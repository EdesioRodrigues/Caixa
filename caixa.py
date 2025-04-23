from tkinter import *
from tkinter import ttk #tkinter libs
from tkinter import messagebox #notificação

import time;
from datetime import date, time, datetime, timedelta #tempo

import contextlib
with contextlib.redirect_stdout(None): #para cancelar msg pygame 
    import pygame, sys, random

#pdf recurso 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4 #para paginas a4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image

import os
import webbrowser


from tkcalendar import Calendar
import sqlite3


pygame.init()
root = Tk()
           
class PlaceholderText(Text):

    def __init__(self, master=None, placeholder='', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_color = self['foreground']
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)
        self.put_placeholder()

    def put_placeholder(self):
        self.delete('1.0', 'end')  # Clear any existing text
        self.insert('1.0', self.placeholder)

    def remove_placeholder(self):
        self.delete('0.0', 'end')
        self['foreground'] = self.default_color

    def focus_in(self, event):
        if self['foreground'] == self.placeholder_color:
            self.delete('0.0', 'end')
            self['foreground'] = self.default_color

    def focus_out(self, event):
        if not self.get('1.0', 'end').strip():
            self.put_placeholder()




#FUNCOES JANELA2
class Func():

    #limpar entradas 
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.quantidade_entry.delete(0, END)
        self.cb_categoria.delete(0, END)
        self.aniversario_entry.delete(0, END)
        self.descricao_txt.delete('1.0', 'end') 

 #---------conect e desconect bd
    def concta_bd(self):
        self.conn = sqlite3.connect("produtos.bd")
        self.cursor = self.conn.cursor()


    def desconecta_bd(self):
        self.conn.close()

    #montagem tabela principal 
    def mont_tabelas(self):
        self.concta_bd()
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                cod INTEGER PRIMARY KEY,
                nome_prod CHAR(40) NOT NULL,
                categoria CHAR(15),
                quantidade INTEGER(1000),
                aniversario DATE(100),
                descricao TEXT(1000)
        );
    """)
        self.conn.commit()
        self.desconecta_bd()

    #variaveis de entrada 
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.categoria  = self.cb_categoria.get()
        self.quantidade = self.quantidade_entry.get()
        self.aniversario = self.aniversario_entry.get()
        self.descricao =self.descricao_txt.get("1.0",END)

    #add produto
    def add_prod(self):
        self.variaveis()
        self.concta_bd()

        self.cursor.execute("""INSERT INTO produtos (nome_prod, categoria, quantidade, aniversario, descricao)
             VALUES(?,?,?,?,?)""",(self.nome, self.categoria, self.quantidade, self.aniversario, self.descricao))
        self.conn.commit()
        self.desconecta_bd()
        self.select_list()
        self.limpar_tela()
        

      #seleciona lista pra view
   
   
   
    def select_list(self):
        self.listaProd.delete(*self.listaProd.get_children())
        self.concta_bd()
        lista = self.cursor.execute(""" SELECT cod,nome_prod, categoria, quantidade, aniversario, descricao FROM produtos
          ORDER BY nome_prod ASC; """)
        for i in lista:
            self.listaProd.insert("", END, values=i)
        self.desconecta_bd()

    #Duplo click e puxa dados da memória  e na tela 
    def duplo_click(self, event):
        self.limpar_tela()
        self.listaProd.selection()

        for n in self.listaProd.selection():
            col1, col2, col3, col4, col5, col6 = self.listaProd.item(n, "values")

            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.cb_categoria.insert(END, col3)
            self.quantidade_entry.insert(END, col4)
            self.aniversario_entry.insert(END, col5)
            self.descricao_txt.insert(END, col6)


    #deleta produto
    def deletar(self):
        self.variaveis()
        self.concta_bd()
        self.cursor.execute(""" DELETE FROM produtos WHERE cod = ? """,(self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_list()

    def del_table(self):
        self.concta_bd()
        self.cursor.execute(""" DELETE FROM produtos WHERE cod = ? """,(self.codigo,))

        
    #altera produto 
    def altera_prod(self):
        self.variaveis()
        self.concta_bd(); print("conctado")
        self.cursor.execute(""" UPDATE produtos SET nome_prod = ?, categoria = ?, quantidade = ?, aniversario = ?, descricao = ?
           WHERE cod = ? """,(self.nome, self.categoria, self.quantidade,self.aniversario, self.descricao,self.codigo))
        print(self.descricao)
        self.conn.commit()
        self.desconecta_bd()
        self.select_list()
        self.limpar_tela()

    #buscar produto
    def busca_prod(self):
        self.concta_bd()
        self.listaProd.delete(*self.listaProd.get_children())
        self.nome_entry.insert(END,"%")
        nome = self.nome_entry.get()
        self.cursor.execute("""SELECT cod, nome_prod, categoria, quantidade, aniversario, descricao FROM produtos
         WHERE nome_prod LIKE '%s' ORDER BY nome_prod ASC""" % nome)
        buscaprod = self.cursor.fetchall()
        for i in buscaprod:
              self.listaProd.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()

    def calendario(self):
        self.calendario1 = Calendar(self.frame1, fg="gray75", bg="white", font=("Times", '9', 'bold'), locale="pt_br")
        self.calendario1.place(relx= 0.5, rely=0.1)
        self.dataDeInicio = Button(self.frame1, text= "Inserir Data", command=self.inserirData)
        self.dataDeInicio.place(relx=0.55, rely=0.85, height=25, width=100)

    def inserirData(self):
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()
        self.aniversario_entry.delete(0, END)
        self.aniversario_entry.insert(END, dataIni)
        self.dataDeInicio.destroy()



#JANELA 2
class relatorios():

    #exibir arqv
    def print_prod(self):
        webbrowser.open("produto.pdf")


    #config pdf e monta ele atrasves do reportlab
    def gerar_relatorio(self):
        self.prod = canvas.Canvas("produto.pdf")

        self.codigo_relatorio = self.codigo_entry.get()
        self.nome_relatorio = self.nome_entry.get()
        self.categoria_relatorio = self.cb_categoria.get()
        self.quantidade_relatorio = self.quantidade_entry.get()
        self.aniversario_relatorio = self.aniversario_entry.get()
        self.descricao_relatorio = self.descricao_txt.get("1.0", "end-1c").replace("\n", "")


         
         #titulo
        self.prod.setFont("Helvetica-Bold", 24)
        self.prod.drawString(200, 790, "Ficha do Produto")

        self.prod.setFont("Helvetica-Bold", 18) #define font
        self.prod.drawString(50, 700, "Codigo:" ) #esq e altura 
        self.prod.drawString(50, 670, "Nome:")
        self.prod.drawString(50, 640, "Categoria:")
        self.prod.drawString(50, 610, "Quantidade:")
        self.prod.drawString(50, 580, "Aniversario:")
        self.prod.drawString(50, 550, "Descrição:")

        self.prod.setFont("Helvetica", 18)
        self.prod.drawString(150, 700, self.codigo_relatorio)
        self.prod.drawString(140, 670, self.nome_relatorio)
        self.prod.drawString(150, 640, self.categoria_relatorio)
        self.prod.drawString(160, 610, self.quantidade_relatorio)
        self.prod.drawString(160, 580, self.aniversario_relatorio)
        self.prod.drawString(160, 550, self.descricao_relatorio)
        print(repr(self.descricao_relatorio))


        self.prod.rect(20,80, 550, 220, fill=False, stroke=True) #linha divisória 

        self.prod.showPage()
        self.prod.save()
        self.print_prod()


    #-------- Funcoes  PRINCIPAL-----------
class functions():

   def on_closing():
        if messagebox.askyesno("Fechar", "Você tem certeza que deseja sair?"):
            root.destroy() 
   root.protocol("WM_DELETE_WINDOW", on_closing)


   #btn sair
   def sair(self):
    if messagebox.askyesno("Fechar", "Você tem certeza que deseja sair?"):
        root.destroy()
        return
      
   
    #btn limpar
   def limpar(self):
       self.recibo_txt.delete("1.0", END)
       self.corte.set("0")
       self.sombrancelha.set("0")
       self.barba.set("0")
       self.outros.set("0")

      #btn total

   def total(self):
      #datas
      self.hoje = datetime.now()
      self.string_hr = self.hoje.strftime("%X")
     
      #get nas var
      Item1 = float (self.corte.get())
      Item2 = float (self.sombrancelha.get())
      Item3 = float (self.barba.get())
      Item4 = float (self.outros.get())

      #cifrao, float e preço dos prod
      self.preço_item1 = ("$") + str('%.2f'%(Item1*25.00))
      self.preço_item2 = ("$") + str('%.2f'%(Item2*15.00))
      self.preço_item3 = ("$") + str('%.2f'%(Item3*15.00))
      self.preço_item4 = ("$") + str('%.2f'%(Item4*10.00))

      #formatando recibo 
      self.opçoes = (Item1*25.00) + (Item2*15.00) + (Item3*15.00) + (Item4*10.00)
      self.subtotal =("$") + str('%.2f'%(self.opçoes))
      x = random.randint(10233, 500298)
      recebe_str = str(x)
      self.recibo_txt.delete("1.0", END)
      self.recibo_txt.insert(END, "CUPOM:"   + recebe_str + "  DATA:" +  self.string_data + "  HORARIO:" + self.string_hr + "\n")
      self.recibo_txt.insert(END, "---------------------------------------------------------------------------" + "\n")
      self.recibo_txt.insert(END, "\nItem:     " + "Preço:"  + "\n")
      self.recibo_txt.insert(END, "---------------------------------------------------------------------------" + "\n")
      self.recibo_txt.insert(END, "Corte de Cabelo:  " + self.preço_item1 + "\n")
      self.recibo_txt.insert(END, "Sombrancelha:  " + self.preço_item2 + "\n")
      self.recibo_txt.insert(END, "Barba:  " + self.preço_item3 + "\n")
      self.recibo_txt.insert(END, "Outros:  " + self.preço_item4 + "\n")
      self.recibo_txt.insert(END, "---------------------------------------------------------------------------" + "\n")
      self.recibo_txt.insert(END, "\nVALOR DA COMPRA:  " + self.subtotal + "\n")


   #relogio
   def relogio(self):
      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")
      self.lb_time.config(text=current_time)
      self.lb_time.after(1000, self.relogio)

   
   def validate_numbers(self,text):
    if text.isnumeric():
        return True
    else:
        return False


   def quit(self): self.main.destroy()

   def gerar_pdf(self):
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))


        # Define o nome do arquivo PDF
        nome_arquivo = 'recibo.pdf'

        # Cria um objeto PDFCanvas
        pdf_canvas = canvas.Canvas(nome_arquivo, pagesize=letter)

        # Recupera o texto do widget recibo_txt
        texto = self.recibo_txt.get("1.0", "end-1c")

        # Define o tamanho da fonte e da linha
        tamanho_fonte = 12
        tamanho_linha = 20

        # Quebra o texto em linhas para evitar que a largura exceda a página
        linhas = texto.split("\n")

        # Define a posição inicial da linha na página
        y = 750

        # Escreve as linhas no PDF
        for linha in linhas:
            pdf_canvas.setFont('Arial', tamanho_fonte)
            pdf_canvas.drawString(100, y, linha)
            y -= tamanho_linha

        # Salva e fecha o arquivo PDF
        pdf_canvas.save()
         # Abre o PDF no navegador padrão do sistema
        file_path = os.path.abspath(nome_arquivo)
        webbrowser.open(file_path)



#--------------- Classe Principal--------
class Aplic(functions, PlaceholderText, Func, relatorios): 
    
    def __init__(self):
      self.root = root
      self.janela()
      self.frames()
      self.widget()
      self.relogio()
      root.mainloop()

    #Janela
    def janela(self):
       self.root.title("Caixa de Vendas")
       self.root.geometry("855x620")
       self.root.configure(background="#219e9c")
       self.root.resizable(False, True) #define se vai ser responsivo
       


    #Frames
    def frames(self):
       self.frame = Frame(self.root, bg="#2b65ed", bd=7, relief=RIDGE) #principal
       self.frame.grid()


       self.frame1 = Frame(self.frame, bg="#0f9499", bd=7, relief=RIDGE)
       self.frame1.grid(row = 0, column=0, columnspan=4, sticky=W)


       self.frame2 = Frame(self.frame, bg="#0f9499", bd=6, relief=RIDGE)
       self.frame2.grid(row = 1, column=1, sticky=W)


       self.frame3 = Frame(self.frame, bg="#0f9499", bd=7, relief=RIDGE)
       self.frame3.grid(row = 1, column=1, sticky=W)


       self.frame4 = Frame(self.frame, bg="#0f9499", bd=7, relief=RIDGE)
       self.frame4.grid(row = 1, column=2, sticky=W)


       self.frame5 = Frame(self.frame4, bg="#0f9499", bd=7, relief=RIDGE)
       self.frame5.grid(row = 0, column=0, sticky=W)


       self.frame6 = Frame(self.frame4, bg="#0f9499", bd=4, relief=RIDGE)
       self.frame6.grid(row = 1, column=0, columnspan=4, sticky=W)


    #--------- Widgets -----------

    def widget(self):
       
    #-----Variaveis ------------
       #datas
       self.data_atual = date.today()
       self.string_data = '{}/{}/{}'.format(self.data_atual.day, self.data_atual.month, self.data_atual.year)
     

      #serviços
       self.corte = StringVar()
       self.sombrancelha = StringVar()
       self.barba = StringVar()
       self.outros = StringVar()

      #set
       self.corte.set("0")
       self.sombrancelha.set("0")
       self.barba.set("0")
       self.outros.set("0")



    #Labels
       self.lb_date = Label (self.frame1, text=self.string_data , fg="#2786ab", font=("arial", 20, "bold"), padx=9, pady=9, width=13, bd=14, bg="#dfe3ee", justify=CENTER) 
       self.lb_date.grid(row=0, column=0)
       
       self.lb_title = Label (self.frame1, text="\tCaixa da Loja\t", font=("arial", 20, "bold"), padx=9, pady=9, bd=14, fg="#2786ab", justify=CENTER)
       self.lb_title.grid(row=0, column=1)

       self.lb_time = Label (self.frame1, text= "", font=("arial", 20, "bold"), padx=9, pady=9, bd=14, fg="#2786ab", justify=CENTER)
       self.lb_time.grid(row=0, column=2)

       self.lb_opcoes = Label (self.frame2, text="Opções:", font=("arial", 20, "bold"), padx=8, pady=1, bd=8,width=25, bg="#2b65ed", fg="white", justify=CENTER)
       self.lb_opcoes.grid(row=0, column=0, columnspan=4)

       self.lb_corte = Label (self.frame2, text="Corte:", font=("arial", 19, "bold"), padx=8, bd=8, bg="#0f9499", fg="white", justify=LEFT)
       self.lb_corte.grid(row=1, column=0)

       self.lb_sombrancelha  = Label (self.frame2, text="Sombrancelha:", font=("arial", 19, "bold"), padx=8, bd=8, bg="#0f9499", fg="white", justify=LEFT)
       self.lb_sombrancelha.grid(row=2, column=0)

       self.lb_barba = Label (self.frame2, text="Barba:", font=("arial", 19, "bold"), padx=8, bd=8, bg="#0f9499", fg="white", justify=LEFT)
       self.lb_barba.grid(row=3, column=0)

       self.lb_outros = Label (self.frame2, text="Outros:", font=("arial", 19, "bold"), padx=8, bd=8, bg="#0f9499", fg="white", justify=LEFT)
       self.lb_outros.grid(row=4, column=0)



     #-------Caixas de texto ----
       self.corte_entry = Entry (self.frame2, textvariable= self.corte, fg="black", font=("arial", 18, "bold"),bd=2, bg="white",justify=CENTER, width=17, validate="key", validatecommand=(self.root.register(self.validate_numbers), "%P"))
       self.corte_entry.grid(row=1, column=1, pady=1)

       self.sombrancelha_entry = Entry (self.frame2, textvariable=self.sombrancelha, fg="black", font=("arial", 18, "bold"), bd=2, bg="white",justify=CENTER, width=17,  validate="key", validatecommand=(self.root.register(self.validate_numbers), "%P"))
       self.sombrancelha_entry.grid(row=2, column=1, pady=1)
       
       self.barba_entry = Entry (self.frame2, textvariable= self.barba, fg="black", font=("arial", 18, "bold"), bd=2, bg="white",justify=CENTER, width=17,  validate="key", validatecommand=(self.root.register(self.validate_numbers), "%P"))
       self.barba_entry.grid(row=3, column=1, pady=1)
       
       self.outros_entry = Entry (self.frame2, textvariable=self.outros, fg="black", font=("arial", 18, "bold"), bd=2, bg="white",justify=CENTER, width=17,  validate="key", validatecommand=(self.root.register(self.validate_numbers), "%P"))
       self.outros_entry.grid(row=4, column=1, pady=1)


      #---------- Recibo ------
       self.recibo_txt = Text(self.frame5, bd=24, font=("arial", 8, "bold"),height=27, width=50)
       self.recibo_txt.grid(row=0, column=0, sticky=W)
      
      



      #---- Botoes ------
       self.total_btn = Button(self.frame6, padx=1, pady=1, bd=4, fg="black", font=("arial", 18, "bold"), width=7, bg="orange", text="Total", command=self.total)
       self.total_btn.grid(row=0, column=0)

       self.limpar_btn = Button(self.frame6, padx=1, pady=1, bd=4, fg="black", font=("arial", 18, "bold"), width=7, bg="yellow", text="Limpar", command=self.limpar)
       self.limpar_btn.grid(row=0, column=2)

       self.sair_btn = Button(self.frame6, padx=1, pady=1, bd=4, fg="black", font=("arial", 18, "bold"), width=7, bg="red", text="Sair", command=self.sair)
       self.sair_btn.grid(row=0, column=3)


       #navbar
       menubar = Menu(self.root)
       self.root.config(menu = menubar )
       filemenu = Menu(menubar )
       filemenu2 = Menu(menubar)
       menubar.add_cascade(label = "Opções", menu = filemenu )
       menubar.add_cascade(label = "Sobre", menu = filemenu2)
       
       filemenu.add_command(label = "CLientes", command=self.abrir_toplevel)
       filemenu.add_command(label = "Limpa CLiente", command=self.limpar)
       filemenu.add_command(label = "Gerar PDF", command=self.gerar_pdf)
       filemenu2.add_command(label = "Sair", command= quit)


     #------------ TOP LEVEL ----------------
    def abrir_toplevel(self):
        #CONFIG JANELA
        self.root2 = Toplevel()
        self.root2.title("Histórico - Guto Barber")
        self.root2.configure(background='#219e9c')
        self.root2.geometry("700x500")
        self.root2.resizable(True, True) #define se vai ser responsivo
        self.root2.maxsize(width=900, height=700)
        self.root2.minsize(width=900, height=400)
        self.root2.transient(self.root)
        self.root2.focus_force()
        self.root2.grab_set()
        self.root2.protocol("WM_DELETE_WINDOW", self.on_closing)

        #FRAMES JANELA
        self.frame1 = Frame(self.root2, bd= 4, bg="#dfe3ee", highlightbackground="#759fe6",highlightthickness=3 )  #place pack grid - USAR PLACE  x,y///// highlightthickness largura da borda
        self.frame1.place(relx= 0.02,  rely=0.02, relwidth=0.96, relheight=0.46) #relx horizontal , rely alig vertical

        self.frame2 = Frame(self.root2, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=3 )
        self.frame2.place(relx= 0.02 , rely= 0.5, relwidth= 0.96, relheight= 0.46)


        #BOTOES
        self.canvas_bt = Canvas(self.frame1, bd=0, bg="#1e3743", highlightbackground="gray", highlightthickness=5)
        self.canvas_bt.place(relx=0.19, rely=0.08, relwidth=0.22, relheight=0.19)

        #criar limpar
        self.bt_limpar = Button(self.frame1, text="Limpar", bd=2, bg="#2786ab", fg="white",
                               font=("verdana", 8, "bold"), command=self.limpar_tela) #função que cria botão
                              
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        #criar buscar
        self.bt_buscar = Button(self.frame1, text="Buscar",bd=2, bg="#2786ab", fg="white", font=("verdana", 8, "bold"), command=self.busca_prod)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

         #criar novo 
        self.bt_novo = Button(self.frame1, text="Novo",bd=2, bg="#2786ab", fg="white", font=("verdana", 8, "bold"), command= self.add_prod)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        # Imagem 

          #criar alterar
        self.bt_alterar = Button(self.frame1, text="Alterar", bd=2, bg="#2786ab", fg="white", font=("verdana", 8, "bold"), command=self.altera_prod)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

          #criar apagar
        self.bt_apagar = Button(self.frame1, text="Apagar", bd=2, bg="#a32a2a", fg="white", font=("verdana", 8, "bold"), command=self.deletar)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)


        #-----------labels e entradas--------

        #Criação da label
        self.lb_codigo = Label(self.frame1, text="Código", bg="#dfe3ee", fg="#2786ab")
        self.lb_codigo.place(relx= 0.05 , rely= 0.05)

        self.codigo_entry = Entry(self.frame1,  bg="lightgray", fg="#2786ab")
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.07)

          #Criação da label nome
        self.lb_nome = Label(self.frame1, text="Nome", bg="#dfe3ee", fg="#2786ab")
        self.lb_nome.place(relx= 0.05 , rely= 0.35)

        self.nome_entry = Entry(self.frame1, bg="lightgray", fg="#2786ab")
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8, relheight=0.11)

          #Criação da label categoria
        self.lb_categoria = Label(self.frame1, text="Categoria", bg="#dfe3ee", fg="#2786ab")
        self.lb_categoria.place(relx= 0.05 , rely= 0.6)

        list = ["Corte", "Barba", "Sombrancelha", "Outros"]

        self.cb_categoria = ttk.Combobox(self.frame1, values=list, font=("Verdana", 8))
        self.cb_categoria.place(relx= 0.05 , rely= 0.7)

           #Criação da label quantidade
        self.lb_quantidade = Label(self.frame1, text="Quantidade", bg="#dfe3ee", fg="#2786ab")
        self.lb_quantidade.place(relx= 0.4 , rely= 0.6)

        self.quantidade_entry = Entry(self.frame1, bg="lightgray", fg="#2786ab", validate="key", validatecommand=(self.root2.register(self.validate_numbers), "%P"))
        self.quantidade_entry.place(relx=0.4, rely=0.7, relwidth=0.1, relheight=0.11)

        #datas aniversaio
        self.btn_aniversario = Button(self.frame1, text="Data", bg="#dfe3ee", fg="#2786ab", command=self.calendario, width=8)
        self.btn_aniversario.place(relx= 0.6 , rely= 0.6)

        self.aniversario_entry = Entry(self.frame1,bg="lightgray", fg="#2786ab")
        self.aniversario_entry.place(relx=0.6, rely=0.7, relwidth=0.1, relheight=0.11)
       

        self.descricao_txt = PlaceholderText(self.root2, placeholder='Descrição...', width=14, height=4,bg="lightgray", fg="#2786ab")
        self.descricao_txt.place(relx=0.8, rely=0.3)


        #LISTA VIEW
        self.listaProd = ttk.Treeview(self.frame2, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaProd.heading("#0", text="")
        self.listaProd.heading("#1", text="Codigo")
        self.listaProd.heading("#2", text="Nome")
        self.listaProd.heading("#3", text="Categoria")
        self.listaProd.heading("#4", text="Quantidade")
        self.listaProd.heading("#5", text="Data")
        self.listaProd.heading("#6", text="Descrição")

        self.listaProd.column("#0", width=1)
        self.listaProd.column("#1", width=50)
        self.listaProd.column("#2", width=200)
        self.listaProd.column("#3", width=125)
        self.listaProd.column("#4", width=125)
        self.listaProd.column("#5", width=125)
        self.listaProd.column("#6", width=125)


        self.listaProd.place(relx=0.001, rely=0.01, relwidth=0.95, relheight=0.97)

        self.listaProd.place(relx=0.001, rely=0.01, relwidth=0.95, relheight=0.97)

        self.scroolLista = Scrollbar(self.frame2, orient="vertical")
        self.scroolLista.config(command=self.listaProd.yview)
        self.listaProd.config(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.01, relwidth=0.04, relheight=0.97)
        self.listaProd.bind("<Double-1>", self.duplo_click)

        #MENU BAR JANELA2
        menubar = Menu(self.root2)
        self.root2.config(menu = menubar )
        filemenu = Menu(menubar )
        filemenu2 = Menu(menubar)


        menubar.add_cascade(label = "Opções", menu = filemenu )
        menubar.add_cascade(label = "Sobre", menu = filemenu2)

        filemenu.add_command(label = "Limpa CLiente", command= self.limpar_tela)
        filemenu.add_command(label = "Gerar PDF", command= self.gerar_relatorio)
        filemenu2.add_command(label = "Sair", command= self.sair)

    def on_closing(self):
            if messagebox.askyesno("Fechar", "Você tem certeza que deseja sair?"):
                self.root2.destroy() 
                self.root2.protocol("WM_DELETE_WINDOW", self.on_closing)

    def sair(self):
     if messagebox.askyesno("Fechar", "Você tem certeza que deseja sair?"):
        self.root2.destroy()


Aplic()

