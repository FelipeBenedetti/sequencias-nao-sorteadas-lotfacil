import csv
import itertools
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Variável global para armazenar os resultados
resultados = []

def ler_resultados(caminho_arquivo):
    global resultados
    resultados = []
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                numeros = list(map(int, row[2:]))
                resultados.append(numeros)
        messagebox.showinfo("Sucesso", "Arquivo CSV carregado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")

def gerar_combinacoes_nao_sorteadas():
    if not resultados:
        messagebox.showwarning("Aviso", "Por favor, carregue um arquivo CSV primeiro.")
        return []
    
    sorteados = [set(concurso) for concurso in resultados]
    todos_numeros = list(range(1, 26))
    todas_combinacoes = itertools.combinations(todos_numeros, 15)
    
    return [combinacao for combinacao in todas_combinacoes if set(combinacao) not in sorteados]

def exibir_sequencias():
    try:
        quantidade = int(quantidade_entry.get())
        if quantidade <= 0:
            messagebox.showwarning("Aviso", "A quantidade deve ser maior que zero.")
            return
    except ValueError:
        messagebox.showwarning("Aviso", "Por favor, insira um número válido.")
        return
    
    nao_sorteadas = gerar_combinacoes_nao_sorteadas()
    if not nao_sorteadas:
        return
    
    if quantidade > len(nao_sorteadas):
        messagebox.showwarning("Aviso", f"Não há combinações suficientes. Máximo disponível: {len(nao_sorteadas)}")
        quantidade = len(nao_sorteadas)
    
    sequencias_aleatorias = random.sample(nao_sorteadas, quantidade)
    
    resultado_text.config(state=tk.NORMAL)
    resultado_text.delete(1.0, tk.END)
    resultado_text.insert(tk.END, f"{quantidade} Sequências não sorteadas:\n\n")
    for i, sequencia in enumerate(sequencias_aleatorias, start=1):
        resultado_text.insert(tk.END, f"{i}: {sorted(sequencia)}\n")
    resultado_text.config(state=tk.DISABLED)

def importar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if caminho_arquivo:
        ler_resultados(caminho_arquivo)

# Criando a interface gráfica aprimorada
root = tk.Tk()
root.title("Gerador de Sequências Não Sorteadas")
root.geometry("580x550")
root.resizable(False, False)
root.configure(bg="#e1e1e1")

style = ttk.Style()
style.theme_use("clam")  # Tema moderno
style.configure("TButton", font=("Arial", 10), padding=5, relief="flat", background="#007acc", foreground="white")
style.map("TButton", background=[("active", "#005f99")])
style.configure("TLabel", font=("Arial", 11), background="#e1e1e1")

# Cabeçalho
header_label = ttk.Label(root, text="🔢 Gerador de Sequências Não Sorteadas 🔢", font=("Arial", 14, "bold"))
header_label.pack(pady=10)

# Frame para importação de arquivo
frame_importacao = ttk.Frame(root)
frame_importacao.pack(pady=5)
importar_button = ttk.Button(frame_importacao, text="📂 Importar CSV", command=importar_arquivo)
importar_button.pack()

# Frame para entrada de quantidade
frame_quantidade = ttk.Frame(root)
frame_quantidade.pack(pady=5)
quantidade_label = ttk.Label(frame_quantidade, text="Quantidade de sequências:")
quantidade_label.pack(side=tk.LEFT, padx=5)
quantidade_entry = ttk.Entry(frame_quantidade, width=10)
quantidade_entry.pack(side=tk.LEFT, padx=5)
quantidade_entry.insert(0, "10")

# Botão para gerar as sequências
gerar_button = ttk.Button(root, text="🎲 Gerar Sequências", command=exibir_sequencias)
gerar_button.pack(pady=10)

# Área de texto com rolagem para exibir as sequências
frame_resultado = ttk.Frame(root)
frame_resultado.pack(pady=5, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(frame_resultado, orient=tk.VERTICAL)
resultado_text = tk.Text(frame_resultado, height=15, width=65, yscrollcommand=scrollbar.set, font=("Courier", 10))
resultado_text.config(state=tk.DISABLED, bg="#f9f9f9", relief="flat", wrap=tk.WORD)
scrollbar.config(command=resultado_text.yview)
resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Rodapé
footer_label = ttk.Label(root, text="🔹 Desenvolvido por Felipe Benedetti ® 🔹", font=("Arial", 9, "italic"))
footer_label.pack(pady=5)

root.mainloop()
