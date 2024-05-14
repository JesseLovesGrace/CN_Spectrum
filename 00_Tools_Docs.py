import re
import os
import csv
from docx import Document
from datetime import datetime

# Directory containing the files
directory = r'C:\Users\jesse\Desktop\Master Thesis\01_Data\Spectrums\Government_Report\Birth_Related'

# Regular expressions to extract information
index_number_pattern = r'索\s+引\s+号：\s*(.*?)\s+'
category_pattern = r'主\s*题\s*分类：\s*(.*?)\s+'
drafting_office_pattern = r'发\s*文\s*机\s*关：\s*(.*?)\s+'
written_date_pattern = r'成\s*文\s*日期：\s*(.*?)\s+'
publish_date_pattern = r'发布日期：\s*(.*?)\s+'
document_number_pattern = r'发文字号：\s*(.*?)\s+'
title_pattern = r'标\s*题：\s*(.*?)\s+'
source_pattern = r'来源：\s*(.*?)\s+'
document_type_pattern = r'公文种类：\s*(.*?)\s+'
date_format_pattern = r'\d{4}-\d{2}-\d{2}'

# Create and open a CSV file for writing
csv_file_path = "report_info.csv"
with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(["文件名", "索引号", "主题分类", "发文机关", "成文日期", "发布日期", "发文字号", "标题", "来源", "公文种类", "内容"])

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith('.docx'):
            try:
                # Read the content of the DOCX file
                doc = Document(filepath)
                text = ' '.join(paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip())

                # Extract information using regular expressions
                index_number_match = re.search(index_number_pattern, text)
                category_match = re.search(category_pattern, text)
                drafting_office_match = re.search(drafting_office_pattern, text)
                written_date_match = re.search(written_date_pattern, text)
                publish_date_match = re.search(publish_date_pattern, text)
                document_number_match = re.search(document_number_pattern, text)
                title_match = re.search(title_pattern, text)
                source_match = re.search(source_pattern, text)
                document_type_match = re.search(document_type_pattern, text)

                # Get the extracted information
                index_number = index_number_match.group(1) if index_number_match else None
                category = category_match.group(1) if category_match else None
                drafting_office = drafting_office_match.group(1) if drafting_office_match else None
                written_date = written_date_match.group(1) if written_date_match else None
                publish_date = publish_date_match.group(1) if publish_date_match else None
                document_number = document_number_match.group(1) if document_number_match else None
                title = title_match.group(1) if title_match else None
                source = source_match.group(1) if source_match else None
                document_type = document_type_match.group(1) if document_type_match else None

                # If 发布日期 is missing but the text contains a date in the format "YYYY-MM-DD", use that as 发布日期
                if not publish_date and re.search(date_format_pattern, text):
                    publish_date = re.search(date_format_pattern, text).group()

                # Write the extracted information to the CSV file
                writer.writerow([filename, index_number, category, drafting_office, written_date,
                                 publish_date, document_number, title, source, document_type, text])

            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

print("CSV file has been created:", csv_file_path)
