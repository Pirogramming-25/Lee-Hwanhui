import re  

def change_float(s):
    return float(s.replace(',', ''))


def parse_nutrition(texts):
    joined = ' '.join(texts)
    flat = joined.replace(' ', '')
    result = {'calories': None, 'carbs': None, 'protein': None, 'fat': None}

    # 칼로리
    kcal_list = re.findall(r'([\d,.]+)kcal', flat)
    if kcal_list:
        result['calories'] = change_float(kcal_list[0])

    # 탄수화물 / 단백질
    for keyword, key in [('탄수화물', 'carbs'), ('단백', 'protein')]:
        m = re.search(keyword + r'[^\d]{0,3}([\d,.]+)(m?g)', flat)
        if m:
            value = change_float(m.group(1))
            unit = m.group(2)
            result[key] = value / 1000 if unit == 'mg' else value

    # 지방
    m = re.search(r'(?<!포화)(?<!트랜스)지방([\d,.]+)(m?g)', flat)
    if m:
        value = change_float(m.group(1))
        unit = m.group(2)
        result['fat'] = value / 1000 if unit == 'mg' else value

    return result