import tkinter as tk                     # Importa o módulo tkinter para criação de interfaces gráficas
from tkinter import messagebox, ttk      # Importa messagebox para exibir caixas de diálogo e ttk para widgets temáticos

# Cria a janela principal (root) da aplicação
root = tk.Tk()
root.title("Gerenciador de Dados")        # Define o título da janela
root.geometry("600x400")                  # Define o tamanho da janela (largura x altura)

# Cria um frame (container) para os campos de entrada (nome e idade) e os posiciona com espaçamento vertical
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

# Rótulos (labels) para os campos de entrada, localizados no frame_inputs em posições específicas na grid
tk.Label(frame_inputs, text="Nome:").grid(row=0, column=0)
tk.Label(frame_inputs, text="Idade:").grid(row=0, column=2)

# Cria os campos de entrada (entry) para nome e idade
entry_nome = tk.Entry(frame_inputs)
entry_idade = tk.Entry(frame_inputs)

# Posiciona os campos de entrada na grid do frame_inputs com espaçamento horizontal (padx)
entry_nome.grid(row=0, column=1, padx=5)
entry_idade.grid(row=0, column=3, padx=5)

# Define as colunas da Treeview que funcionará como uma "tabela" de dados
cols = ("ID", "Nome", "Idade")

# Cria a Treeview com as colunas definidas, sem exibir a coluna "principal" (show="headings")
tree = ttk.Treeview(root, columns=cols, show="headings")

# Configura os títulos de cada coluna da Treeview
for col in cols:
    tree.heading(col, text=col)

# Posiciona a Treeview na janela principal, permitindo que ela expanda e preencha o espaço disponível com padding
tree.pack(expand=True, fill="both", padx=10, pady=10)

# Variável global para controlar o ID dos registros adicionados
id_counter = 1

def adicionar():
    """
    Função para adicionar um novo registro na Treeview.
    Recupera os valores dos campos de entrada e, se ambos estiverem preenchidos,
    insere um novo registro com um ID incremental. Caso contrário, exibe um aviso.
    """
    global id_counter 
    nome = entry_nome.get()         # Obtém o texto do campo 'nome'
    idade = entry_idade.get()       # Obtém o texto do campo 'idade'
    if nome and idade:              # Verifica se ambos os campos foram preenchidos
        # Insere uma nova linha na Treeview com os valores: ID, nome e idade
        tree.insert("", "end", values=(id_counter, nome, idade))
        id_counter += 1             # Incrementa o contador de IDs para o próximo registro
        # Limpa os campos de entrada
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
    else:
        # Exibe uma mensagem de aviso se algum campo estiver vazio
        messagebox.showwarning("Aviso", "Preencha todos os campos.")

def deletar():
    """
    Função para deletar o registro selecionado na Treeview.
    Se um registro estiver selecionado, remove-o; caso contrário, exibe um aviso.
    """
    selecionado = tree.selection()  # Obtém os itens selecionados na Treeview
    if selecionado:
        tree.delete(selecionado)    # Deleta o(s) item(ns) selecionado(s)
    else:
        messagebox.showwarning("Aviso", "Selecione um item para deletar.")

def editar():
    """
    Função para editar o registro selecionado.
    Em vez de remover o registro e inserir um novo (o que altera o ID), a função agora atualiza
    os valores de 'Nome' e 'Idade' mantendo o mesmo ID.
    """
    selecionado = tree.selection()  # Obtém o item selecionado
    if selecionado:
        # Obtém os valores atuais do registro (estrutura: [ID, Nome, Idade])
        valores = tree.item(selecionado)["values"]
        novo_nome = entry_nome.get()   # Novo nome a partir do campo de entrada
        nova_idade = entry_idade.get()   # Nova idade a partir do campo de entrada
        if novo_nome and nova_idade:
            # Atualiza o registro selecionado mantendo o mesmo ID
            tree.item(selecionado, values=(valores[0], novo_nome, nova_idade))
            # Limpa os campos de entrada após a atualização
            entry_nome.delete(0, tk.END)
            entry_idade.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos para editar.")
    else:
        messagebox.showwarning("Aviso", "Selecione um item para editar.")

def localizar():
    """
    Função para localizar e selecionar um registro na Treeview com base no nome.
    Procura pelo termo digitado no campo 'Nome'. Se encontrado, seleciona e foca o item;
    caso contrário, exibe uma mensagem informando que o nome não foi localizado.
    """
    termo = entry_nome.get()        # Termo de pesquisa extraído do campo 'Nome'
    encontrado = False              # Flag para indicar se algum registro foi encontrado
    for item in tree.get_children():  # Itera sobre todos os itens da Treeview
        # Compara ignorando maiúsculas/minúsculas se o termo está contido no nome do registro
        if termo.lower() in str(tree.item(item)["values"][1]).lower():
            tree.selection_set(item)  # Seleciona o item
            tree.focus(item)          # Foca na seleção
            encontrado = True         # Define a flag como encontrado
            break                     # Interrompe o loop após encontrar o primeiro item correspondente
    if not encontrado:
        messagebox.showinfo("Não encontrado", "Nome não Localizado")

# Cria um frame para os botões e os posiciona com espaçamento vertical
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=5)

# Cria os botões e os posiciona dentro do frame de botões com espaçamento horizontal
tk.Button(frame_botoes, text="Adicionar", command=adicionar).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text="Editar", command=editar).grid(row=0, column=1, padx=5)
tk.Button(frame_botoes, text="Deletar", command=deletar).grid(row=0, column=2, padx=5)
tk.Button(frame_botoes, text="Localizar", command=localizar).grid(row=0, column=3, padx=5)

root.mainloop()  # Inicia o loop principal da interface gráfica, mantendo a janela aberta
