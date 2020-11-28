import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        candidate = {}
        candidate['info'] = text[:text.find('Желаемая должность и зарплата')].replace(u'\xa0', u' ')
        var = candidate['info'].split(',')
        if 'Мужчина' in var[0]:
            candidate['name'] = var[0][0:-7]
            candidate['gender'] = 'Мужчина'
        else:
            candidate['name'] = var[0][0:-7]
            candidate['gender'] = 'Женщина'
        var_2_split = var[2].split(' ')
        for i in var_2_split:
            if '@' in i:
                candidate['email'] = i[7:len(i)]
        phone = var_2_split[4][-1] + var_2_split[5][1:4] + var_2_split[6][0:6]
        if phone.isdigit():
            candidate['phone'] = phone
        else:
            candidate['phone'] = 'None'
        candidate['desired_position_and_salary'] = text[text.find('Желаемая должность и зарплата') + len('Желаемая должность и зарплата')
                                                        :text.find('Опыт работы')].replace(u'\xa0', u' ')
        candidate['experience'] = text[text.find('Опыт работы — ')+len('Опыт работы — ')
                                       :text.find('Образование')].replace(u'\xa0', u' ')
        if text.find('Повышение квалификации, курсы') != -1:
            candidate['education'] = text[text.find('Образование')+len('Образование')
                                          :text.find('Повышение квалификации, курсы')].replace(u'\xa0', u' ')
            candidate['training'] = text[text.find('Повышение квалификации, курсы')+len('Повышение квалификации, курсы')
                                         :text.find('Ключевые навыки')]\
                .replace(u'\xa0', u' ')
        else:
            candidate['education'] = text[text.find('Образование')+len('Образование'):text.find('Ключевые навыки')]\
                .replace(u'\xa0', u' ')

        candidate['key_skills'] = text[text.find('Ключевые навыки')+len('Ключевые навыки'):text.find('Дополнительная информация')]\
            .replace(u'\xa0', u' ')
        candidate['key_skills'] = {'languages': candidate['key_skills'][candidate['key_skills'].find('Знание языков')+len('Знание языков'):candidate['key_skills'].find('Навыки')],
                                   'skills': candidate['key_skills'][candidate['key_skills'].find('Навыки')+len('Навыки'):]}
        candidate['additional_information'] = text[text.find('Дополнительная информация')+len('Дополнительная информация'):]\
            .replace(u'\xa0', u' ')
        # candidate['additional_information'] = candidate['additional_information'].\
        #     replace(candidate['additional_information'][candidate['additional_information'].
        #             find('•  Резюме обновлено'):candidate['additional_information'].find(u'\x0c')+1], '')

        for i in candidate:
            if i=='key_skills': continue
            if candidate[i].find('  •  Резюме обновлено') != -1:
                candidate[i] = candidate[i].replace(candidate[i][candidate[i].find('  •  Резюме обновлено'):candidate[i].find(u'\x0c')+1], '')
            if candidate[i].find('Резюме обновлено') != -1:
                candidate[i] = candidate[i].replace(candidate[i][candidate[i].find('Резюме обновлено'):candidate[i].find(u'\x0c')+1], '')

        return candidate
    return None