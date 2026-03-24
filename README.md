# Minería de Reglas de Asociación

Aplicación web modular para el análisis y extracción de patrones y reglas de asociación a partir de bases de datos transaccionales. Desarrollada sin dependencias externas (utilizando únicamente la biblioteca estándar de Python) y enfocada tanto en la obtención rápida de métricas analíticas como en el aprendizaje guiado de algoritmos de minería de datos.

## 🚀 Características Principales

La aplicación implementa los 3 algoritmos fundamentales de minería de itemsets frecuentes:
- **A Priori:** Exploración iterativa por niveles estructurada mediante filtrado de candidatos.
- **FP-Growth:** Compresión transaccional mediante Árboles de Patrones Frecuentes (FP-Trees) sin generación explícita de candidatos.
- **ECLAT:** Intersección vertical de TIDs (Transaction IDs) para búsqueda rápida orientada en profundidad.

### Modos de Visualización (UI Dual)
La interfaz gráfica cuenta con dos modalidades en tiempo real:
- **Modo Resultados:** Enfocado al usuario analítico. Genera directamente las Reglas de Asociación finales, detallando el cálculo exacto de métricas clave: *Soporte*, *Confianza* y *Lift*.
- **Modo Procedimiento (Didáctico):** Desglosa paso a paso el esqueleto matemático interno de cada algoritmo de manera visual:
  - Generación, conteo y filtro iterativo de candidatos (con código de colores ✓/✗).
  - Representación visual del *FP-Tree Inicial* dibujado mediante nodos estilizados.
  - Tabla relacional exacta de Extracción de Patrones Condicionales (Minería).

## 🛠️ Estructura del Proyecto

El código fuente ha sido factorizado en una arquitectura limpia y modular:

```text
/Reglas asociativas/
├── app.py                  # Servidor HTTP nativo y punto de entrada principal
├── algorithms/             # Paquete lógico (Backend)
│   ├── __init__.py
│   ├── apriori.py          # Lógica, logs y métricas de A Priori
│   ├── fpgrowth.py         # Clases FPNode, FPTree y lógica de FP-Growth
│   └── eclat.py            # Manejo de Tid-lists e intersecciones ECLAT
├── templates/
│   └── index.html          # Interfaz (Frontend), Estilos CSS Vanilla y lógica JS
└── README.md
```

## ⚙️ Instalación y Uso

Dado que el ecosistema no usa bibliotecas externas, simplemente requiere de **Python 3.x**.

1. Abre tu terminal.
2. Navega al directorio del proyecto:
   ```bash
   cd "/Reglas asociativas"
   ```
3. Inicia el servidor nativo de Python:
   ```bash
   python3 app.py
   ```
4. Abre tu navegador de preferencia y visita: [http://localhost:8765](http://localhost:8765)

## 📌 Autor y Colaboradores
Pablo Francisco Decena Romero
