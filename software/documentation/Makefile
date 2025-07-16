# Makefile para generación de hojas de datos
# Método optimizado con generate_professional_pdf.py únicamente

.PHONY: all professional pdf clean help install install-minimal

# Variables
README = README.md
BUILD_DIR = build

# Comando por defecto - versión profesional optimizada
all: professional

# Método PROFESIONAL optimizado (único método disponible)
professional:
	@echo "🏆 Generando hoja de datos PROFESIONAL..."
	@mkdir -p $(BUILD_DIR)
	@python generate_professional_pdf.py
	@echo "✅ Listo! Calidad profesional con imágenes de hardware/resources/"

# Generar PDF directamente con Chrome
pdf:
	@echo "📄 Generando PDF con Chrome..."
	@mkdir -p $(BUILD_DIR)
	@python generate_professional_pdf.py
	@if command -v google-chrome-stable >/dev/null 2>&1; then \
		echo "🔧 Convirtiendo HTML a PDF con Chrome..."; \
		cd $(BUILD_DIR) && google-chrome-stable --headless --disable-gpu --print-to-pdf=datasheet.pdf --no-margins --print-to-pdf-no-header datasheet_professional.html; \
		echo "✅ PDF generado: $(BUILD_DIR)/datasheet.pdf"; \
	elif command -v chromium-browser >/dev/null 2>&1; then \
		echo "🔧 Convirtiendo HTML a PDF con Chromium..."; \
		cd $(BUILD_DIR) && chromium-browser --headless --disable-gpu --print-to-pdf=datasheet.pdf --no-margins --print-to-pdf-no-header datasheet_professional.html; \
		echo "✅ PDF generado: $(BUILD_DIR)/datasheet.pdf"; \
	else \
		echo "⚠️ Chrome/Chromium no encontrado. Solo HTML disponible."; \
		echo "📄 HTML disponible: $(BUILD_DIR)/datasheet_professional.html"; \
	fi

# Instalar dependencias mínimas
install:
	@echo "📦 Instalando dependencias mínimas..."
	@pip install -r requirements.txt
	@echo "✅ Dependencias instaladas (markdown2, PyYAML, Pillow)"

# Limpiar archivos generados
clean:
	@echo "🧹 Limpiando archivos generados..."
	@rm -rf $(BUILD_DIR)
	@echo "✅ Limpieza completada"

# Generar y abrir automáticamente
open: professional
	@echo "🌐 Abriendo hoja de datos profesional..."
	@python -c "import webbrowser, os; webbrowser.open('file://' + os.path.abspath('build/datasheet_professional.html'))"

# Verificar que README.md existe
check:
	@if [ ! -f $(README) ]; then \
		echo "❌ Error: $(README) no encontrado"; \
		exit 1; \
	fi
	@echo "✅ $(README) encontrado"

# Mostrar información de ayuda
help:
	@echo "🛠️ GENERADOR DE HOJAS DE DATOS - OPTIMIZADO"
	@echo "==========================================="
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make professional    - Genera hoja PROFESIONAL (HTML) ⭐"
	@echo "  make pdf             - Genera hoja + PDF con Chrome"
	@echo "  make open            - Genera y abre en navegador"
	@echo "  make install         - Instala dependencias mínimas"
	@echo "  make clean           - Limpia archivos generados"
	@echo "  make check           - Verifica que README.md existe"
	@echo "  make help            - Muestra esta ayuda"
	@echo ""
	@echo "⭐ RECOMENDADO:"
	@echo "  make professional    (ultra-rápido, < 0.1 segundos)"
	@echo ""
	@echo "🚀 Características:"
	@echo "  - Solo 3 dependencias Python"
	@echo "  - Sin Sphinx, sin LaTeX"
	@echo "  - Imágenes automáticas desde hardware/"
	@echo "  - Escalado uniforme TOP/BOTTOM view"
	@echo "  - Saltos de página optimizados"
	@echo "  - Compatible con GitHub Pages"
