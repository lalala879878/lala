from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import g4f
from g4f.Provider import ChatForAi

app = Flask(__name__)

@app.route('/quest', methods=['POST'])
def handle_post_request():
  data = request.get_json()
  text = data['text']
  message = g4f.ChatCompletion.create(
      model=g4f.models.default,
      messages=[{"role": "system", "content": 'You are a NASA assistant called 9G who is in a spaceship, answer the question in less than 90 characters. say it like robot'},
                {"role": "user", "content": text}],
      temperature=1,
      provider=ChatForAi
  )
  response_data = {'message': 'Данные успешно получены', 'received_text': message}
  return jsonify(response_data)

@app.route('/')
def index():
  message = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{"role": "system", "content": 'You are a NASA assistant called 9G who is in a spaceship, answer the question in less than 90 characters, say hello and your name. say it like robot'}],
        temperature=1,
        provider=ChatForAi
    )
  return render_template('nasa.html', message=message)

@app.route('/cabinet')
def cabinet():
  all_table_data = []
  for page_number in range(2):
    url = f'https://standards.nasa.gov/all-standards?order=field_document_date&sort=asc&page={page_number}'
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table')
    table_data = []

    for row in table.find_all('tr'):
        row_data = []
        cells = row.find_all('td')
        for cell in cells:
            row_data.append(cell.text)
        table_data.append(row_data)

    all_table_data.extend(table_data)
    
  return render_template('cabinet.html', table_data=all_table_data)

@app.route('/nasa_cabinet')
def nasa_cabinet():
    t1 = []
    t2 = []  
    t3 = []  
    t4 = []  
    t5 = []  
    t6 = []  
    t7 = []    
    t8 = []
    t9 = []
    
    column_data = [[] for _ in range(9)]  # Создайте список для хранения данных
    
    urls = ['https://standards.nasa.gov/systems-engineering-and-integration',
            'https://standards.nasa.gov/computer-systems-software-information-systems',
            'https://standards.nasa.gov/human-factors-and-health',
            'https://standards.nasa.gov/electrical-and-electronics-systems',
            'https://standards.nasa.gov/structures-mechanical-systems',
            'https://standards.nasa.gov/materials-and-processes-parts',
            'https://standards.nasa.gov/systems-and-subsystem-test',
            'https://standards.nasa.gov/safety-quality-reliability-maintainability',
            'https://standards.nasa.gov/construction-institutional-support']
    
    for i in range(len(urls)):
      url = urls[i]
      response = requests.get(url)
      html = response.text
      soup = BeautifulSoup(html, 'html.parser')
      table = soup.find('table')
  
      if table:
          for row in table.find_all('tr'):
              cells = row.find_all('td')
              if cells:
                  first_cell = cells[0].text
                  third_cell = cells[2].text
                  link = cells[0].find('a')
                  if link:
                      link_url = link.get('href')
                      combined_data = {'text': f"{third_cell} {first_cell}", 'link': 'https://standards.nasa.gov'+link_url}
                  else:
                      combined_data = {'text': f"{third_cell} {first_cell}", 'link': None}
                  column_data[i].append(combined_data)
      else:
          print(f"Таблица {i + 1} не найдена на странице.")

    return render_template('nasa_cabinet.html', column_data=column_data)

@app.route('/login')
def login():
  return render_template('login.html')

app.run(host='0.0.0.0', port=81)
