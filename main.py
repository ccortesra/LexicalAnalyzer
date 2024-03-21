import re

class LexicalAnalyzer:
  def __init__(self,text_lines):
    self.text_lines = text_lines
    self.reserved_words = ['fun', 'escribir', 'poner','caso','verdadero', 'desde', 'falso','mientras','rango','sino','si','hasta','repetir', 'cierto', 'falso', 'imprimir', 'leer', 'retornar', 'funcion', 'en', 'para','fin', 'retorno']
    self.operators = [
    ("tkn_and", "&&"),
    ("tkn_or", "\\|\\|"),
    ("tkn_concat", "\\.\\."),
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
    self.num_exp = r'\d+(\.\d+)?'
    self.variable_exp = r'[a-zA-Z_][0-9a-zA-Z_]*'
# ------------------------------------------------------------------------------------------
  def find_reserved_words(self, line, i, j):
    for exp in self.reserved_words:
        # Compilar la expresión regular para incluir los límites de palabra
        pattern = re.compile(f'\\b{exp}\\b')
        # Buscar la coincidencia desde el índice actual 'j'
        coincidencia = pattern.search(line, pos=j)
        if coincidencia:
            inicio = coincidencia.start()  # Obtener la posición de inicio de la coincidencia
            # Verificar si el inicio coincide con el índice actual 'j'
            if inicio == j:
                texto_coincidente = coincidencia.group()  # Obtener el texto que coincide
                print(f'<{texto_coincidente},{i+1},{j+1}>')
                j += (coincidencia.end()-inicio)
                return j
    return j
  
  def find_numbers(self,line,i,j):
    coincidencia = re.match(self.num_exp, line[j:])
    if coincidencia:
      inicio = coincidencia.start()  # Obtener la posición de inicio de la coincidencia
      texto_coincidente = coincidencia.group()  # Obtener el texto que coincide
      print(f'<tkn_real,{texto_coincidente},{i+1},{j+inicio+1}>')
      j += coincidencia.end() 
      return j
    return j

  def find_operators(self,line,i,j):
    for op, exp in self.operators:
      coincidencia = re.match(exp, line[j:])
      if coincidencia:
        inicio = coincidencia.start()  # Obtener la posición de inicio de la coincidencia
        print(f'<{op},{i+1},{j+inicio+1}>')
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
  
  def find_tkn_string(self,line,i,j):
    if line[j-1] == '"':
      coincidencia = re.match(r'.*?(?=")', line[j:])
    else:
      coincidencia = re.match(r".*?(?=')", line[j:])
    if coincidencia:
      inicio = coincidencia.start()  # Obtener la posición de inicio de la coincidencia
      texto_coincidente = coincidencia.group()  # Obtener el texto que coincide
      print(f'<tkn_str,{texto_coincidente},{i+1},{j+inicio}>')
      j += coincidencia.end()
      return j+1
    else:
      return j-1

  
  # ----------------------------------------------------------------
  # FUNCIÓN PRINCIPAL
  # ----------------------------------------------------------------
  def find_tokens(self):
    multi_comment = False
    for i in range(len(self.text_lines)):
      line = self.text_lines[i]
      if line.strip() == '':
        continue
      # if line.startswith('//'):  # Ignorar comentarios
      #   continue
      # if line.startswith('#'):  # Ignorar comentarios
      #   continue



      j = 0

      while j < len(line):
        # Palabras reservadas
        try:
          if line[j:].startswith('*/'):  # Ignorar comentarios
            multi_comment = False
            j+=2  
            continue
        
          elif line[j:].startswith('/*') or multi_comment:  # Ignorar comentarios
            multi_comment = True
            j+=1 # Aqui vale la pena seguir mirando la misma linea?
            continue

          

          elif line[j:].startswith('//'):  # Ignorar comentarios
            break
          elif line[j:].startswith('#'):  # Ignorar comentarios
            break

          elif line[j] == ' ':
            j+= 1
            continue

          elif line[j] == '"' or line[j] == "'":
            starting_j = j
            j = self.find_tkn_string(line,i,j+1)
            if j == starting_j:
              print(f'>>> Error lexico (linea: {i+1}, posicion: {j+1})')
              return

          else:
            starting_j = j
            j = self.find_reserved_words(line,i,j)
            j = self.find_numbers(line,i,j)
            j = self.find_operators(line,i,j)
            j = self.find_identifiers(line,i,j)
            if starting_j == j:
              print(f'>>> Error lexico (linea: {i+1}, posicion: {j+1})')
              return

        except:
          continue


if __name__ == '__main__':
  input_line = """para i en rango(10)
poner(i .. '\n')
fin
"""
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