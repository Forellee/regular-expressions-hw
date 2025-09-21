from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

new_contacts_list = []
for contact in contacts_list:
    full_name = " ".join(contact[:3]).split()
    while len(full_name) < 3:
        full_name.append("")
    lastname, firstname, surname = full_name[:3]
    new_contact = [lastname, firstname, surname] + contact[3:]
    new_contacts_list.append(new_contact)

# ФОрматирование телефонов
phone_pattern = re.compile(
    r"(\+7|8)\s*\(?(?P<code>\d{3})\)?[-\s]*(?P<part1>\d{3})[-\s]*(?P<part2>\d{2})[-\s]*(?P<part3>\d{2})(\s*\(?(доб.)\s*(?P<ext>\d+)\)?)?"
)

substitution = r"+7(\g<code>)\g<part1>-\g<part2>-\g<part3>\g<ext_block>"

def format_phone(phone):
    match = phone_pattern.search(phone)
    if match:
        code = match.group("code")
        part1 = match.group("part1")
        part2 = match.group("part2")
        part3 = match.group("part3")
        ext = match.group("ext")
        if ext:
            return f"+7({code}){part1}-{part2}-{part3} доб.{ext}"
        else:
            return f"+7({code}){part1}-{part2}-{part3}"
    return phone

for contact in new_contacts_list:
    contact[5] = format_phone(contact[5])

# Убираем дубли
contacts_dict = {}
for contact in new_contacts_list:
    key = (contact[0], contact[1])
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        old_contact = contacts_dict[key]
        contacts_dict[key] = [
            old if old else new for old, new in zip(old_contact, contact)
        ]

final_contacts_list = list(contacts_dict.values())

pprint(final_contacts_list)

# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)