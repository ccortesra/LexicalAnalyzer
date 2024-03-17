import re

def read_text_from_file(filename):
  with open(filename, 'r') as file:
      text = file.read()
  return text

def write_text_to_file(text, filename):
  with open(filename, 'w') as file:
      file.write(text)


class LexicalAnalyzer:
  def __init__(self,text_lines):
    self.text_lines = text_lines
    self.reserved_words = ['escribir','caso','verdadero',   'falso','mientras','rango','sino','si','hasta','repetir', 'cierto', 'falso', 'imprimir', 'leer', 'retornar', 'funcion']

  def find_tokens(self):
    for i in range(len(self.text_lines)):
      line = self.text_lines[i]
      if line[0] == '/' and line[1] == '/':
        continue
      words = line.split()
      
      for word in words:
        if word in self.reserved_words:
          coincidencia= re.search(r'\b' + re.escape(word) + r'\b', line)
          start_char = coincidencia.start()
          print(f'<{word},{i+1},{start_char+1}>')

 


if __name__ == '__main__':
  input_text = open('./case 1.txt','r')
  input_line = input_text.readlines()
  #input_line = input()
  print(input_line)
  lexical_analyzer = LexicalAnalyzer(input_line)
  lexical_analyzer.find_tokens()