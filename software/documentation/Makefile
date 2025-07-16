# Makefile para generación de hojas de datos
# Usando el script general de back/documentation

.PHONY: all pdf clean help install professional

# Variables
README = README.md
BUILD_DIR = build
BACK_DOC_PATH = ../../../../back/documentation
PYTHON_VENV = ../../../../.venv/bin/python

# Comando por defecto
all: pdf

# Generar PDF usando el script general
pdf:
	@echo "📄 Generando hoja de datos con script general..."
	@mkdir -p $(BUILD_DIR)
	@cd $(BACK_DOC_PATH) && $(PYTHON_VENV) generate_pdf.py $(CURDIR)/$(README)
	@if [ -f build/*.pdf ]; then \
		echo "✅ PDF generado en build/"; \
	else \
		echo "❌ Error: No se encontró el PDF generado"; \
	fi

# Método PROFESIONAL (mantener compatibilidad)
professional:
	@echo "🏆 Generando hoja de datos PROFESIONAL..."
	@mkdir -p $(BUILD_DIR)
	@python generate_professional_pdf.py
	@echo "✅ Listo! Calidad profesional con imágenes de hardware/resources/"

# Instalar dependencias
install:
	@echo "📦 Instalando dependencias..."
	@pip install -r requirements.txt
	@echo "✅ Dependencias instaladas"

# Limpiar archivos generados
clean:
	@echo "🧹 Limpiando archivos generados..."
	@rm -rf $(BUILD_DIR)
	@echo "✅ Limpieza completada"

# Verificar que README.md existe
check:
	@if [ ! -f $(README) ]; then \
		echo "❌ Error: $(README) no encontrado"; \
		exit 1; \
	fi
	@echo "✅ $(README) encontrado"

# Mostrar información de ayuda
help:
	@echo "🛠️ GENERADOR DE HOJAS DE DATOS"
	@echo "=============================="
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make pdf             - Genera PDF usando script general (SIN sección adicional)"
	@echo "  make professional    - Genera hoja PROFESIONAL (CON sección adicional)"
	@echo "  make install         - Instala dependencias"
	@echo "  make clean           - Limpia archivos generados"
	@echo "  make check           - Verifica que README.md existe"
	@echo "  make help            - Muestra esta ayuda"
	@echo ""
	@echo "⭐ RECOMENDADO para evitar 'ADDITIONAL PRODUCT DOCUMENTATION':"
	@echo "  make pdf"
