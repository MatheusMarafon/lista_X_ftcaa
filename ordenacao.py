import time
import random
import statistics
import pandas as pd
import matplotlib.pyplot as plt

def bubble_sort(arr, max_time=300):
    start = time.perf_counter()
    n = len(arr)
    swaps = 0
    for i in range(n):
        if time.perf_counter() - start > max_time:
            raise TimeoutError()
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return swaps

def merge_sort(arr):
    movements = 0
    def sort(sub_arr):
        nonlocal movements
        if len(sub_arr) > 1:
            mid = len(sub_arr) // 2
            L = sub_arr[:mid]
            R = sub_arr[mid:]
            movements += len(L) + len(R)

            sort(L)
            sort(R)

            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    sub_arr[k] = L[i]
                    i += 1
                else:
                    sub_arr[k] = R[j]
                    j += 1
                k += 1
                movements += 1

            while i < len(L):
                sub_arr[k] = L[i]
                i += 1
                k += 1
                movements += 1

            while j < len(R):
                sub_arr[k] = R[j]
                j += 1
                k += 1
                movements += 1
    sort(arr)
    return movements

def quick_sort(arr):
    swaps = 0
    import sys
    sys.setrecursionlimit(200000)
    
    def partition(low, high):
        nonlocal swaps
        pivot_idx = (low + high) // 2
        pivot = arr[pivot_idx]
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        swaps += 1
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        return i + 1

    def sort(low, high):
        if low < high:
            pi = partition(low, high)
            sort(low, pi - 1)
            sort(pi + 1, high)
            
    sort(0, len(arr) - 1)
    return swaps

def main():
    tamanhos = [1000, 10000, 100000]
    algoritmos = ["Bubble Sort", "Merge Sort", "Quick Sort"]
    resultados = []

    print("Iniciando testes experimentais...\n")

    for tam in tamanhos:
        random.seed(42)
        vetores_originais = [[random.randint(1, 1000000) for _ in range(tam)] for _ in range(3)]
        
        for alg in algoritmos:
            tempos = []
            operacoes = []
            timeout_ocorrido = False

            for rodada in range(3):
                vetor_copia = list(vetores_originais[rodada])
                
                try:
                    if alg == "Bubble Sort":
                        t_inicio = time.perf_counter()
                        ops = bubble_sort(vetor_copia, max_time=300)
                        t_fim = time.perf_counter()
                    elif alg == "Merge Sort":
                        t_inicio = time.perf_counter()
                        ops = merge_sort(vetor_copia)
                        t_fim = time.perf_counter()
                    elif alg == "Quick Sort":
                        t_inicio = time.perf_counter()
                        ops = quick_sort(vetor_copia)
                        t_fim = time.perf_counter()
                    
                    tempos.append(t_fim - t_inicio)
                    operacoes.append(ops)
                except TimeoutError:
                    timeout_ocorrido = True
                    break

            if timeout_ocorrido:
                resultados.append({
                    "Algoritmo": alg,
                    "Tamanho": tam,
                    "Execucao 1 (s)": "Timeout (>300s)",
                    "Execucao 2 (s)": "Timeout (>300s)",
                    "Execucao 3 (s)": "Timeout (>300s)",
                    "Media (s)": "Timeout (>300s)",
                    "Desvio Padrao (s)": "N/A",
                    "Operacoes (Trocas/Mov)": "N/A"
                })
                print(f"{alg} com {tam} elementos: TIMEOUT (> 300 segundos)")
            else:
                media_t = statistics.mean(tempos)
                desvio_t = statistics.stdev(tempos) if len(tempos) > 1 else 0.0
                media_ops = int(statistics.mean(operacoes))
                
                resultados.append({
                    "Algoritmo": alg,
                    "Tamanho": tam,
                    "Execucao 1 (s)": round(tempos[0], 6),
                    "Execucao 2 (s)": round(tempos[1], 6),
                    "Execucao 3 (s)": round(tempos[2], 6),
                    "Media (s)": round(media_t, 6),
                    "Desvio Padrao (s)": round(desvio_t, 6),
                    "Operacoes (Trocas/Mov)": media_ops
                })
                print(f"{alg} com {tam} elementos finalizado. Média: {media_t:.6f}s")

    df = pd.DataFrame(resultados)
    excel_path = "PlanilhaListaDeExerciciosX.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"\nDados salvos com sucesso no Excel: {excel_path}")

    # Gerar Grafico de Linhas Comparativo (com escala logaritmica no eixo Y para melhor visualizacao)
    plt.figure(figsize=(10, 6))
    
    for alg in algoritmos:
        filtrado = [r for r in resultados if r["Algoritmo"] == alg]
        x_vals = [r["Tamanho"] for r in filtrado]
        y_vals = []
        for r in filtrado:
            if isinstance(r["Media (s)"], str) and "Timeout" in r["Media (s)"]:
                y_vals.append(300.0) # Representa graficamente como o limite de 300s
            else:
                y_vals.append(r["Media (s)"])
                
        plt.plot(x_vals, y_vals, marker='o', label=alg)

    plt.xscale('log')
    plt.yscale('log')
    plt.title("Tempo Médio de Execução vs Tamanho do Vetor (Escala Logarítmica)")
    plt.xlabel("Tamanho do Vetor (N)")
    plt.ylabel("Tempo Médio (s)")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    
    grafico_path = "ordenacao_grafico.png"
    plt.savefig(grafico_path, dpi=300, bbox_inches="tight")
    print(f"Gráfico comparativo salvo em: {grafico_path}")

if __name__ == "__main__":
    main()
