import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


def verificar_triangulo(a: float, b: float, c: float) -> bool:
    """
    Verifica se três segmentos podem formar um triângulo usando a desigualdade triangular.
    
    Args:
        a, b, c: Comprimentos dos segmentos
        
        
    Returns:
        bool: True se os segmentos podem formar um triângulo
    """
    return (a + b > c) and (a + c > b) and (b + c > a)


def calcular_vertice(a: float, b: float, c: float) -> tuple[float, float]:
    """
    Calcula as coordenadas do terceiro vértice do triângulo.
    
    Args:
        a, b, c: Comprimentos dos lados do triângulo
        
    Returns:
        tuple: Coordenadas (x, y) do vértice C
    """
    angulo = np.arccos((a**2 + c**2 - b**2) / (2 * a * c))
    return a * np.cos(angulo), a * np.sin(angulo)


def plotar_triangulo(a: float, b: float, c: float, ax: plt.Axes) -> None:
    """
    Plota um triângulo com os lados fornecidos.
    
    Args:
        a, b, c: Comprimentos dos lados
        ax: Eixos do matplotlib para plotagem
    """
    vertices = np.array([[0, 0], [c, 0], calcular_vertice(a, b, c)])
    triangulo = Polygon(vertices, closed=True, alpha=0.4, color='seagreen', edgecolor='darkgreen')
    ax.add_patch(triangulo)
    
    # Anotações dos lados
    ax.text(c/2, -0.2, 'c = {:.1f}'.format(c), ha='center', fontweight='bold', fontsize=10)
    ax.text(vertices[2,0]/2, vertices[2,1]/2, 'a = {:.1f}'.format(a), 
            ha='right', va='center', fontweight='bold', fontsize=10)
    ax.text((c + vertices[2,0])/2, vertices[2,1]/2, 'b = {:.1f}'.format(b), 
            ha='left', va='center', fontweight='bold', fontsize=10)
    
    ax.set_xlim(-0.5, max(c, vertices[2,0]) + 0.5)
    ax.set_ylim(-0.5, vertices[2,1] + 0.5)
    ax.set_title('TRIANGULO VALIDO', fontsize=14, color='darkgreen', pad=15)


def plotar_segmentos(a: float, b: float, c: float, ax: plt.Axes) -> None:
    """
    Plota os três segmentos separadamente quando não formam triângulo,
    incluindo a linha da soma dos dois menores lados.
    
    Args:
        a, b, c: Comprimentos dos segmentos
        ax: Eixos do matplotlib para plotagem
    """
    # Identifica os dois menores lados e o maior
    lados_ordenados = sorted([a, b, c])
    menor1, menor2, maior = lados_ordenados
    soma_menores = menor1 + menor2
    
    # Encontra qual variável original é o maior lado
    if a == maior:
        label_maior = 'a'
    elif b == maior:
        label_maior = 'b'
    else:
        label_maior = 'c'
    
    # Encontra labels dos menores lados
    labels_menores = []
    valores_menores = []
    for lado, valor in zip(['a', 'b', 'c'], [a, b, c]):
        if valor in [menor1, menor2]:
            labels_menores.append(lado)
            valores_menores.append(valor)
    
    offsets = [0.3, 0.15, 0, -0.1]
    cores = ['steelblue', 'mediumseagreen', 'firebrick', 'darkorange']
    valores = [a, b, c, soma_menores]
    labels = [
        'a = {:.1f}'.format(a), 
        'b = {:.1f}'.format(b), 
        'c = {:.1f}'.format(c),
        '{} + {} = {:.1f}'.format(labels_menores[0], labels_menores[1], soma_menores)
    ]
    
    # Plotar os segmentos individuais e a soma
    for valor, offset, cor, label in zip(valores, offsets, cores, labels):
        ax.plot([0, valor], [offset, offset], linewidth=3, color=cor, label=label)
        ax.text(valor/2, offset + 0.05, '{:.1f}'.format(valor), 
               ha='center', va='bottom', fontweight='bold', fontsize=9,
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Destacar visualmente a comparação entre a soma e o maior lado
    ax.axvline(x=maior, color='firebrick', linestyle=':', alpha=0.7, linewidth=2)
    ax.axvline(x=soma_menores, color='darkorange', linestyle=':', alpha=0.7, linewidth=2)
    
    ax.set_xlim(0, max(maior, soma_menores) + 1)
    ax.set_ylim(-0.2, 0.5)
    ax.set_title('NAO FORMA TRIANGULO - {} > {} + {}'.format(
        label_maior, labels_menores[0], labels_menores[1]), fontsize=12, color='darkred', pad=15)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))


def main():
    """Função principal do verificador de triângulos."""
    print("\n" + "=" * 50)
    print("VERIFICADOR DE TRIANGULO")
    print("=" * 50)
    
    try:
        a = float(input("\n  Primeiro segmento: "))
        b = float(input("  Segundo segmento:  "))
        c = float(input("  Terceiro segmento: "))
        
        if a <= 0 or b <= 0 or c <= 0:
            print("\n  Erro: Comprimentos devem ser valores positivos")
            return
            
    except ValueError:
        print("\n  Erro: Entrada invalida - digite valores numericos")
        return

    forma_triangulo = verificar_triangulo(a, b, c)
    
    # Configuração da figura
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_xlabel('Comprimento', fontsize=11)
    
    # Plotagem baseada no resultado
    if forma_triangulo:
        plotar_triangulo(a, b, c, ax)
    else:
        plotar_segmentos(a, b, c, ax)

    plt.tight_layout()
    plt.show()
    
    # Relatório final
    print("\n  Segmentos: a = {:.1f}, b = {:.1f}, c = {:.1f}".format(a, b, c))
    
    if not forma_triangulo:
        lados_ordenados = sorted([a, b, c])
        soma_menores = lados_ordenados[0] + lados_ordenados[1]
        maior = lados_ordenados[2]
        
        # Identifica labels corretos
        if a == maior:
            label_maior = 'a'
            labels_menores = ['b', 'c'] if b == lados_ordenados[0] else ['c', 'b']
        elif b == maior:
            label_maior = 'b'
            labels_menores = ['a', 'c'] if a == lados_ordenados[0] else ['c', 'a']
        else:
            label_maior = 'c'
            labels_menores = ['a', 'b'] if a == lados_ordenados[0] else ['b', 'a']
        
        print("  Soma dos dois menores lados: {:.1f}".format(soma_menores))
        print("  Maior lado: {:.1f}".format(maior))
        print("  Condicao violada: {} > {} + {}".format(
            label_maior, labels_menores[0], labels_menores[1]))
    
    print("  Resultado: {}".format(
        "PODE formar triangulo" if forma_triangulo else "NAO forma triangulo"
    ))
    print("=" * 50)
    print()


if __name__ == "__main__":
    main()
