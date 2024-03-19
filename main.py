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
    self.reserved_words = ['escribir','caso','verdadero',   'falso','mientras','rango','sino','si','hasta','repetir', 'cierto', 'falso', 'imprimir', 'leer', 'retornar', 'funcion', 'en', 'para','fin']
    self.operators = [
    ("tkn_and", "&&"),
    ("tkn_or", "\\|\\|"),
    ("tkn_concat", "\\.."),
    ("tkn_period", "\\."),
    ("tkn_comma", ","),
    ("tkn_semicolon", ";"),
    ("tkn_colon", ":"),
    ("tkn_opening_key", "{"),
    ("tkn_closing_key", "}"),
    ("tkn_opening_bra", "\\["),
    ("tkn_closing_bra", "\\]"),
    ("tkn_opening_par", "\\("),
    ("tkn_closing_par", "\\)"),
    ("tkn_increment", "\\+\\+"),
    ("tkn_decrement", "--"),
    ("tkn_mod_assign", "%="),
    ("tkn_div_assign", "/="),
    ("tkn_times_assign", "\\*="),
    ("tkn_minus_assign", "-="),
    ("tkn_plus_assign", "\\+="),
    ("tkn_plus", "\\+"),
    ("tkn_minus", "-"),
    ("tkn_times", "\\*"),
    ("tkn_div", "/"),
    ("tkn_power", "\\^"),
    ("tkn_mod", "%"),
    ("tkn_equal", "=="),
    ("tkn_neq", "!="),
    ("tkn_leq", "<="),
    ("tkn_geq", ">="),
    ("tkn_greater", ">"),
    ("tkn_less", "<"),
    ("tkn_regex", "~="),
    ("tkn_assign", "="),
    ("tkn_not", "!")
]
    self.real_exp = r'[0-9]*.[0-9]*'
    self.variable_exp = r'[a-zA-Z_][0-9a-zA-Z_]*'
# ------------------------------------------------------------------------------------------
  def find_reserved_words(self, line,i, j):
    for exp in self.reserved_words:
      coincidencia = re.match(f'\b{exp}\b(?![\w_])', line[j:])
      if coincidencia:
        inicio = coincidencia.start()  # Obtener la posición de inicio de la coincidencia
        texto_coincidente = coincidencia.group()  # Obtener el texto que coincide
        print(f'<{texto_coincidente},{i+1},{j+inicio+1}>')
        j += coincidencia.end()
        return j
    return j
      
  def find_operators(self,line,i,j):
    for op, exp in self.operators:
      coincidencia = re.match(exp, line[j:])
      if coincidencia:
        inicio = coincidencia.start()  # Obtener la posición de inicio de la coincidencia
        texto_coincidente = coincidencia.group()  # Obtener el texto que coincide
        print(f'<{op},{texto_coincidente},{i+1},{j+inicio+1}>')
        j += coincidencia.end()
        return j
    return j

  def find_identifiers(self,line,i,j):
    coincidencia = re.match(self.variable_exp, line[j:])
    if coincidencia:
      inicio = coincidencia.start()  # Obtener la posición de inicio de la coincidencia
      texto_coincidente = coincidencia.group()  # Obtener el texto que coincide
      print(f'<id,{texto_coincidente},{i+1},{j+inicio+1}>')
      j += coincidencia.end()
      return j
    return j

  def find_tokens(self):
    for i in range(len(self.text_lines)):
      line = self.text_lines[i]
      if line == '':
        continue
      if line.startswith('//'):  # Ignorar comentarios
        continue
      if line.startswith('#'):  # Ignorar comentarios
        continue
      
      

      j = 0
    
      while j < len(line):
        # Palabras reservadas
        try:
          if line[j] == ' ':
            j+= 1
            continue
          j = self.find_reserved_words(line,i,j)
          print(line[j])

          # Números
          if re.match('\d', line[j]):
            coincidencia = re.match(self.real_exp, line[j:])
            inicio = coincidencia.start()  # Obtener la posición de inicio de la coincidencia
            texto_coincidente = coincidencia.group()  # Obtener el texto que coincide
            print(f'<tkn_real,{texto_coincidente},{i+1},{j+inicio+1}>')
            j += coincidencia.end() - 1
          print(line[j])
          # Operadores
          j = self.find_operators(line,i,j)
          print(line[j])
          j = self.find_identifiers(line,i,j)
          print(line[j])

        except:
          continue

if __name__ == '__main__':
  #input_text = open('./case 1.txt','r')
#   input_line = """hola()                              #
# escribir(nombreFuncion(4.56,53.98))"""
  input_line = """// Este caso de prueba evalúa que las palabras
## reservadas se impriman de manera correcta.

escribira verdadero en falso

   hasta
         leer una_variable_x



para
      procesarla :)"""
  #input_line = input()
  input_line = input_line.split('\n')
  lexical_analyzer = LexicalAnalyzer(input_line)
  lexical_analyzer.find_tokens()


# if __name__ == '__main__':
#   #input_text = open('./case 1.txt','r')
#   #input_line = input_text.readlines()
#   try:
#     source_code = ""
#     while True:
#         entrada = input()
#         source_code += entrada+"\n"
#   except EOFError:
#     pass
#   print(source_code)
#   lexical_analyzer = LexicalAnalyzer(source_code)
#   lexical_analyzer.find_tokens()