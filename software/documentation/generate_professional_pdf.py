#!/usr/bin/env python3
"""
Generador PROFESIONAL de hojas de datos para DISTRIBUCIÓN
Especializado en documentación técnica comercial con imágenes de hardware/resources
Optimizado para pinout, dimensiones y especificaciones técnicas
"""

import os
import re
import yaml
import shutil
from datetime import datetime
from zoneinfo import ZoneInfo


class RepositoryExplorer:
    """Explorador automático de estructura de repositorios"""
    
    def __init__(self, base_path):
        self.base_path = base_path
        self.repo_root = self.find_repository_root()
        self.discovered_content = {}
        
    def find_repository_root(self):
        """Encuentra la raíz del repositorio"""
        current = os.path.abspath(self.base_path)
        
        # Primero intentar ir hacia arriba hasta encontrar .git o README.md principal
        while current != os.path.dirname(current):
            # Verificar si hay .git (repositorio git)
            if os.path.exists(os.path.join(current, '.git')):
                print(f"📁 Raíz del repositorio encontrada (.git): {current}")
                return current
            
            # Verificar si hay un README.md Y directorios típicos de proyecto
            if (os.path.exists(os.path.join(current, 'README.md')) and 
                os.path.exists(os.path.join(current, 'hardware')) and
                os.path.exists(os.path.join(current, 'software'))):
                print(f"📁 Raíz del repositorio encontrada (estructura): {current}")
                return current
            
            current = os.path.dirname(current)
        
        # Si no se encuentra, usar el directorio base y subir dos niveles
        # (desde software/documentation -> ../../)
        fallback = os.path.abspath(os.path.join(self.base_path, '..', '..'))
        if os.path.exists(os.path.join(fallback, 'README.md')):
            print(f"📁 Usando raíz fallback: {fallback}")
            return fallback
        
        print(f"⚠️ No se encontró raíz del repositorio, usando: {os.path.abspath(self.base_path)}")
        return os.path.abspath(self.base_path)
    
    def scan_repository_structure(self):
        """Escanea toda la estructura del repositorio buscando README files"""
        readme_files = []
        
        # Buscar README files en toda la estructura
        for root, dirs, files in os.walk(self.repo_root):
            # Ignorar directorios típicos que no contienen documentación útil
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.vscode', 'build']]
            
            for file in files:
                if file.lower().startswith('readme') and file.lower().endswith('.md'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.repo_root)
                    readme_files.append({
                        'path': file_path,
                        'relative_path': relative_path,
                        'directory': os.path.dirname(relative_path) or 'root',
                        'priority': self.get_priority(relative_path)
                    })
        
        # Ordenar por prioridad (root > hardware > software > otros)
        readme_files.sort(key=lambda x: x['priority'])
        return readme_files
    
    def get_priority(self, relative_path):
        """Asigna prioridad a los README según su ubicación"""
        if relative_path == 'README.md':
            return 1  # Máxima prioridad al README principal
        elif 'hardware' in relative_path.lower():
            return 2
        elif 'software' in relative_path.lower():
            return 3
        elif 'examples' in relative_path.lower():
            return 4
        else:
            return 5
    
    def extract_all_sections(self, content, source_info):
        """Extrae todas las secciones de un README"""
        sections = {}
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Detectar títulos (## o ###)
            if line.strip().startswith('##'):
                # Guardar sección anterior si existe
                if current_section:
                    sections[current_section] = {
                        'content': '\n'.join(current_content).strip(),
                        'source': source_info,
                        'level': current_section.count('#')
                    }
                
                # Iniciar nueva sección
                current_section = line.strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Guardar última sección
        if current_section:
            sections[current_section] = {
                'content': '\n'.join(current_content).strip(),
                'source': source_info,
                'level': current_section.count('#')
            }
        
        return sections
    
    def discover_repository_content(self):
        """Descubre todo el contenido del repositorio organizadamente"""
        readme_files = self.scan_repository_structure()
        all_sections = {}
        
        print(f"🔍 Scanning repository structure from: {self.repo_root}")
        
        for readme_info in readme_files:
            try:
                with open(readme_info['path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Limpiar comentarios HTML
                content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
                
                source_info = {
                    'file': readme_info['relative_path'],
                    'directory': readme_info['directory'],
                    'priority': readme_info['priority']
                }
                
                sections = self.extract_all_sections(content, source_info)
                
                print(f"📄 Found {len(sections)} sections in {readme_info['relative_path']}")
                
                # Merge sections con resolución de conflictos
                for section_title, section_data in sections.items():
                    section_key = self.normalize_section_key(section_title)
                    
                    if section_key not in all_sections:
                        all_sections[section_key] = section_data
                    else:
                        # Resolver conflictos por prioridad
                        existing_priority = all_sections[section_key]['source']['priority']
                        new_priority = section_data['source']['priority']
                        
                        if new_priority < existing_priority:  # Menor número = mayor prioridad
                            all_sections[section_key] = section_data
                            print(f"  ✅ Replaced {section_key} with higher priority version")
                        else:
                            print(f"  ⚠️ Kept existing {section_key} (higher priority)")
                            
            except Exception as e:
                print(f"❌ Error reading {readme_info['path']}: {e}")
        
        self.discovered_content = all_sections
        print(f"🎯 Total discovered sections: {len(all_sections)}")
        return all_sections
    
    def normalize_section_key(self, section_title):
        """Normaliza títulos de sección para búsqueda consistente"""
        # Remover # y limpiar
        key = re.sub(r'^#+\s*', '', section_title).strip().lower()
        
        # Normalizar variaciones comunes
        normalizations = {
            'key features': 'features',
            'main features': 'features',
            'technical features': 'features',
            'pin configuration': 'pinout',
            'pin layout': 'pinout',
            'pins': 'pinout',
            'electrical characteristics': 'specifications',
            'electrical specs': 'specifications',
            'specs': 'specifications',
            'tech specs': 'specifications',
            'component reference': 'components',
            'parts list': 'components',
            'bill of materials': 'components',
            'usage examples': 'usage',
            'how to use': 'usage',
            'getting started': 'usage',
            'typical applications': 'applications',
            'use cases': 'applications',
            'communication interfaces': 'interfaces',
            'connectivity': 'interfaces'
        }
        
        return normalizations.get(key, key)
    
    def find_section_by_keywords(self, keywords):
        """Busca secciones que contengan palabras clave específicas"""
        found_sections = {}
        
        for section_key, section_data in self.discovered_content.items():
            for keyword in keywords:
                if keyword.lower() in section_key or keyword.lower() in section_data['content'].lower():
                    found_sections[section_key] = section_data
                    break
        
        return found_sections
    
    def get_best_section(self, preferred_keys):
        """Obtiene la mejor sección disponible de una lista de preferencias"""
        for key in preferred_keys:
            normalized_key = self.normalize_section_key(key)
            if normalized_key in self.discovered_content:
                return self.discovered_content[normalized_key]
        return None


class ProfessionalDatasheetGenerator:
    def __init__(self, base_path=None):
        self.css_professional = self.get_professional_css()
        self.base_path = base_path or os.path.dirname(os.path.abspath(__file__))
        
        # Inicializar explorador de repositorio
        self.explorer = RepositoryExplorer(self.base_path)
        self.repo_root = self.explorer.repo_root
        
        # Buscar automáticamente la carpeta de hardware en múltiples ubicaciones
        self.hardware_path = self.find_hardware_directory()
        
    def discover_project_information(self):
        """Descubre automáticamente toda la información del proyecto"""
        print("🚀 Starting automatic project discovery...")
        
        # Escanear toda la estructura del repositorio
        all_sections = self.explorer.discover_repository_content()
        
        # Extraer información clave del proyecto
        project_info = self.extract_project_metadata(all_sections)
        
        return {
            'sections': all_sections,
            'metadata': project_info,
            'explorer': self.explorer
        }
    
    def extract_project_metadata(self, all_sections):
        """Extrae metadatos del proyecto desde las secciones descubiertas"""
        metadata = {
            'title': 'Electronic Module',
            'subtitle': 'Professional electronic component',
            'version': '1.0',
            'description': 'Advanced electronic module for various applications'
        }
        
        # Leer directamente el README principal para extraer el título
        main_readme_path = os.path.join(self.repo_root, 'README.md')
        if os.path.exists(main_readme_path):
            try:
                with open(main_readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                # Extraer título (primera línea que empieza con # y no ##)
                lines = readme_content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('# ') and not line.startswith('## '):
                        title = line[2:].strip()
                        if title and len(title) > 3:
                            metadata['title'] = title
                            break
                
                # Buscar descripción en la sección Introduction
                intro_match = re.search(r'## Introduction\s*\n\n(.*?)(?:\n\n|\n##)', readme_content, re.DOTALL)
                if intro_match:
                    desc = intro_match.group(1).strip()
                    # Limpiar markdown del texto
                    desc = self.clean_markdown_content(desc)
                    if desc and len(desc) > 20:
                        metadata['description'] = desc[:200] + '...' if len(desc) > 200 else desc
                        
            except Exception as e:
                print(f"⚠️ Error leyendo README principal: {e}")
        
        return metadata
        
        # Buscar título en README principal
        main_content = self.explorer.discovered_content.get('root', {}).get('content', '')
        if main_content:
            lines = main_content.split('\n')
            for line in lines[:10]:  # Buscar en las primeras líneas
                if line.strip() and not line.startswith('#') and not line.startswith('<'):
                    # Primera línea significativa como descripción
                    metadata['description'] = line.strip()
                    break
                elif line.startswith('# '):
                    # Título principal
                    metadata['title'] = line.replace('# ', '').strip()
        
        return metadata
        
    def find_hardware_directory(self):
        """Encuentra automáticamente el directorio de hardware"""
        possible_paths = [
            "../../hardware/resources",  # Estructura estándar
            "../../hardware",            # Carpeta hardware directa
            "../hardware/resources",     # Un nivel menos
            "../hardware",               # Un nivel menos, directa
            "./hardware/resources",      # Mismo nivel
            "./hardware",                # Mismo nivel, directa
            "../../../hardware/resources",  # Dos niveles arriba
            "../../../hardware"          # Dos niveles arriba, directa
        ]
        
        for path in possible_paths:
            abs_path = os.path.abspath(os.path.join(self.base_path, path))
            if os.path.exists(abs_path):
                print(f"📁 Hardware directory found: {abs_path}")
                return path
        
        # Si no encuentra ninguna, usar la ruta estándar
        print(f"⚠️ Hardware directory not found, using default: ../../hardware/resources")
        return "../../hardware/resources"
        
    def get_professional_css(self):
        """CSS profesional para documentación técnica comercial"""
        return """
        @page {
            size: A4;
            margin: 20mm 15mm;
            
            @top-left {
                content: "UNIT Electronics";
                font-size: 9pt;
                color: #666;
                font-weight: bold;
            }
            
            @top-right {
                content: "Technical Datasheet - " attr(data-product);
                font-size: 9pt;
                color: #666;
            }
            
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 12pt;
                color: #999;
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Roboto', 'Segoe UI', 'Arial', sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            font-size: 11pt;
            background: white;
        }
        
        .container {
            max-width: 210mm;
            margin: 0 auto;
            padding: 0;
        }
        
        /* PAGE STRUCTURE FOR BETTER PRINT LAYOUT */
        .page-section {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            page-break-after: auto;
        }
        
        @media print {
            .page-section {
                min-height: auto;
                page-break-inside: avoid;
            }
        }
        
        /* ENCABEZADO PROFESIONAL - TONOS OSCUROS */
        .header {
            background: white;
            color: #374151;
            padding: 20px 30px;
            position: relative;
            overflow: hidden;
            border-radius: 8px;
        }
        
        .header::before {
            display: none;
        }
        
        .header-grid {
            display: grid;
            grid-template-columns: auto 1fr auto;
            align-items: center;
            gap: 20px;
            position: relative;
            z-index: 2;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .company-logo {
            width: 120px;
            height: 75px;
            object-fit: contain;
            background: white;
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 8px rgba(124, 45, 18, 0.15);
        }
        
        .company-info {
            font-size: 9pt;
            opacity: 0.9;
            color: #4b5563;
        }
        
        .product-title-section {
            text-align: center;
        }
        
        .product-code {
            font-size: 14pt;
            font-weight: bold;
            background: white;
            color: #1f2937;
            padding: 4px 12px;
            border-radius: 15px;
            display: inline-block;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        
        .product-title {
            font-size: 24pt;
            font-weight: bold;
            margin-bottom: 5px;
            color: #111827;
            text-shadow: 0 1px 2px rgba(17, 24, 39, 0.1);
        }
        
        .product-subtitle {
            font-size: 14pt;
            color: #4b5563;
            font-style: italic;
            opacity: 0.9;
        }
        
        .version-section {
            text-align: right;
            font-size: 8pt;
            color: #374151;
        }
        
        .version-badge {
            background: white;
            color: #1f2937;
            padding: 6px 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            font-weight: 500;
        }
        
        /* ESPECIFICACIONES DESTACADAS - ESPACIADO COMPACTO */
        .key-specs {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(107, 114, 128, 0.1);
        }
        
        .specs-title {
            text-align: center;
            font-size: 18pt;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 15px;
            border-bottom: 3px solid #6b7280;
            padding-bottom: 8px;
            letter-spacing: 0.5px;
        }
        
        .specs-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .spec-group {
            background: white;
            border-radius: 8px;
            padding: 15px;
            border: 1px solid #e5e7eb;
        }
        
        .spec-group h4 {
            color: #374151;
            font-size: 14pt;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: bold;
        }
        
        .spec-item {
            display: flex;
            justify-content: space-between;
            margin: 4px 0;
            font-size: 11pt;
            padding: 2px 0;
            line-height: 1.4;
        }
        
        .spec-item strong {
            color: #1f2937;
            font-weight: 600;
        }
        
        .spec-item span {
            color: #374151;
            text-align: right;
        }
        
        .spec-label {
            color: #374151;
            font-weight: 500;
        }
        
        .spec-value {
            font-weight: bold;
            color: #111827;
        }
        
        /* SECCIÓN DE IMÁGENES TÉCNICAS - ESPACIADO COMPACTO */
        .images-section {
            margin: 15px 0;
            background: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(192, 132, 252, 0.1);
        }
        
        .images-title {
            text-align: center;
            font-size: 16pt;
            font-weight: bold;
            color: #374151;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding-bottom: 6px;
        }
        
        .images-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .image-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .image-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .image-card-title {
            font-size: 12pt;
            font-weight: bold;
            color: #374151;
            margin-bottom: 10px;
            text-align: center;
            text-transform: uppercase;
            padding-bottom: 5px;
        }
        
        .technical-image {
            width: 100%;
            max-height: 250px;
            object-fit: contain;
            border-radius: 6px;
            background: #ffffff;
            padding: 8px;
        }
        
        .image-caption {
            font-size: 8pt;
            color: #6b7280;
            text-align: center;
            margin-top: 8px;
            font-style: italic;
        }
        
        /* TABLAS PROFESIONALES - ESPACIADO REDUCIDO */
        .table-section {
            margin: 15px 0;
            page-break-inside: avoid;
        }
        
        .section-title {
            font-size: 16pt;
            font-weight: bold;
            color: #374151;
            background: white;
            padding: 12px 20px;
            margin: 15px 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-radius: 0 8px 8px 0;
        }
        
        /* ADDITIONAL SECTIONS (USAGE, DOWNLOADS) - No page break */
        .additional-sections {
            page-break-before: avoid !important;
            page-break-inside: avoid !important;
            margin: 20px 0;
            min-height: 100px;
        }
        
        .professional-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 10px 0;
            background: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
            font-size: 11pt;
        }
        
        .professional-table th {
            background: white;
            color: #374151;
            padding: 15px 12px;
            text-align: center;
            font-weight: bold;
            font-size: 12pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
        }
        
        .professional-table th::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        }
        
        .professional-table td {
            padding: 12px 10px;
            border-bottom: 1px solid #f1f5f9;
            font-size: 11pt;
            vertical-align: middle;
            position: relative;
        }
        
        .professional-table tbody tr:nth-child(even) {
            background: #f8fafc;
        }
        
        .professional-table tbody tr:hover {
            background: #f3f4f6;
            transform: scale(1.01);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* ESTILOS ESPECÍFICOS PARA PINOUT */
        .pinout-table .pin-number {
            color: #374151 !important;
            font-weight: bold;
            text-align: center;
            font-size: 10pt;
            padding: 8px;
        }
        
        .pinout-table .pin-name {
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: #374151;
            text-align: center;
            font-size: 9pt;
        }
        
        .pinout-table .pin-function {
            color: #374151;
            font-size: 8pt;
            text-align: left;
            padding-left: 15px;
        }
        
        /* CARACTERÍSTICAS EN GRID - ESPACIADO COMPACTO */
        .features-section {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            page-break-after: avoid;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        
        .feature-card {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        .feature-title {
            font-weight: bold;
            color: #374151;
            margin-bottom: 6px;
            font-size: 11pt;
            line-height: 1.4;
        }
        
        .feature-desc {
            font-size: 10pt;
            color: #374151;
            line-height: 1.5;
        }
        
        /* APLICACIONES - ESPACIADO COMPACTO */
        .applications-section {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            page-break-before: avoid;
        }
        
        .applications-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        
        .app-card {
            background: white;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            font-size: 10pt;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            line-height: 1.4;
        }

        /* TABLES SECTION */
        .tables-section {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            page-break-before: avoid;
        }

        .table-container {
            margin-bottom: 20px;
        }

        .table-title {
            font-size: 12pt;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .technical-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 9pt;
            background: white;
        }

        .technical-table thead {
            background: #f3f4f6;
        }

        .technical-table th {
            padding: 8px 12px;
            text-align: left;
            font-weight: bold;
            color: #1f2937;
            border: 1px solid #d1d5db;
        }

        .technical-table td {
            padding: 6px 12px;
            border: 1px solid #d1d5db;
            color: #374151;
            line-height: 1.4;
        }

        .technical-table tr:nth-child(even) {
            background: #f9fafb;
        }

        /* PINOUT TABLE STYLES */
        .pinout-table-section {
            margin: 20px 0;
            background: #f0fdf4;
            padding: 15px;
            border-radius: 8px;
        }

        .pinout-table-section .table-title {
            margin-bottom: 10px;
            color: #059669;
            font-size: 14pt;
            font-weight: bold;
        }

        .pinout-table-section table {
            margin: 0 auto;
            width: 100%;
        }

        /* COMPONENTS TABLE STYLES */
        .components-table-section {
            margin: 20px 0;
            background: #f0fdf4;
            padding: 15px;
            border-radius: 8px;
        }

        .components-table-section .table-title {
            margin-bottom: 10px;
            color: #059669;
        }

        /* APPLICATIONS TABLE STYLES */
        .applications table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }

        .applications th {
            background: #fef3c7;
            color: #92400e;
            padding: 10px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #f59e0b;
        }

        .applications td {
            padding: 8px 10px;
            border: 1px solid #f59e0b;
            line-height: 1.4;
        }

        .applications tr:nth-child(even) {
            background: #fffbeb;
        }
        
        .app-title {
            font-weight: bold;
            color: #374151;
            margin-bottom: 4px;
            font-size: 11pt;
        }
        
        /* PIE DE PÁGINA PROFESIONAL */
        .footer {
            margin-top: 40px;
            padding: 20px 30px;
            background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
            color: white;
            border-radius: 12px 12px 0 0;
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: 20px;
        }
        
        .footer-left,
        .footer-right {
            font-size: 8pt;
        }
        
        .footer-center {
            text-align: center;
            font-weight: bold;
            font-size: 10pt;
        }
        
        /* PRINT OPTIMIZATIONS - COMPACT LAYOUT WITH NO BLANK PAGES */
        @media print {
            @page {
                size: A4;
                margin: 12mm 10mm;
            }
            
            * {
                box-shadow: none !important;
                text-shadow: none !important;
            }
            
            body { 
                font-size: 12pt !important; 
                line-height: 1.4;
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }
            
            .container { 
                padding: 0; 
                max-width: none;
                margin: 0;
            }
            
            .no-print { 
                display: none !important; 
            }
            
            /* Compact header for print */
            .header {
                padding: 10px 15px;
                margin-bottom: 5mm;
                page-break-inside: avoid;
                page-break-after: avoid;
            }
            
            .product-title {
                font-size: 24pt !important;
            }
            
            /* COMPACT CONTENT SECTIONS - IMPROVED SECTION BREAKS */
            .content-section {
                page-break-inside: avoid;
                page-break-after: auto;
                margin: 0 0 8mm 0;
                padding: 4mm;
                background: none !important;
                border: none !important;
            }
            
            .visual-section {
                page-break-inside: avoid;
                page-break-before: auto;
                margin: 0;
                padding: 4mm;
                background: none !important;
                border: none !important;
            }
            
            /* BETTER SECTION SEPARATION */
            .introduction-section,
            .product-views-section,
            .key-specs,
            .table-section,
            .features-section,
            .applications-section {
                page-break-after: avoid;
                page-break-inside: avoid;
                margin-bottom: 6mm !important;
            }
            
            /* FORCE BETTER SECTION FLOW */
            .features-section + .applications-section {
                page-break-before: avoid !important;
                margin-top: 2mm !important;
            }
            
            .table-section + .table-section {
                page-break-before: avoid !important;
                margin-top: 3mm !important;
            }
            
            /* VISUAL CONTENT GROUPING */
            .visual-content {
                page-break-before: auto;
                page-break-inside: avoid;
                margin-top: 4mm !important;
            }
            
            /* ELIMINAR ALL WHITE SPACE - COMPACT LAYOUT */
            .visual-content {
                margin: 0 !important;
                padding: 0 !important;
                page-break-before: avoid !important;
            }
            
            .section-title-major {
                font-size: 12pt;
                margin: 5mm 0 3mm 0 !important;
                padding: 2mm 0;
                page-break-before: always;
                page-break-after: avoid;
            }
            
            .table-section, .features-section, .applications-section {
                margin: 2mm 0 !important;
                padding: 2mm !important;
                page-break-inside: avoid;
                background: none !important;
                border: none !important;
            }
            
            /* ENSURE FEATURES AND APPLICATIONS STAY TOGETHER */
            .features-section + .applications-section {
                page-break-before: avoid !important;
                margin-top: 1mm !important;
            }
            
            .section-title {
                font-size: 10pt;
                margin: 2mm 0 1mm 0 !important;
                padding: 1mm 2mm !important;
                page-break-after: avoid;
            }
            
            /* ADDITIONAL SECTIONS (USAGE, DOWNLOADS) - No page break */
            .additional-sections {
                page-break-before: avoid;
                page-break-inside: avoid;
                margin: 5mm 0;
            }
            
            /* TOPOLOGY SECTION - LARGE IMAGE */
            .topology-section {
                page-break-inside: avoid;
                page-break-before: auto;
                margin: 5mm 0;
                padding: 5mm;
            }
            
            .topology-image-large {
                max-width: 170mm !important;
                height: auto;
                padding: 3mm;
                margin: 3mm auto;
            }
            
            /* SCHEMATIC SECTION - PAGE BREAK */
            .schematic-section {
                page-break-before: always !important;
                page-break-inside: avoid;
                margin: 5mm 0;
                padding: 5mm;
            }
            
            .schematic-image {
                max-width: 80mm !important;
                height: auto;
                padding: 3mm;
                margin: 3mm auto;
            }
            
            .features-grid, .applications-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 2mm;
                margin: 2mm 0 !important;
            }
            
            .feature-card, .app-card {
                padding: 1.5mm !important;
                margin: 0 !important;
                page-break-inside: avoid;
                background: none !important;
                box-shadow: none !important;
            }
            
            .feature-title, .app-title {
                font-size: 8pt;
                margin-bottom: 1mm !important;
            }
            
            .feature-desc {
                font-size: 7pt;
                line-height: 1.2;
            }
            
            .product-code {
                font-size: 12pt;
                padding: 2px 8px;
            }
            
            /* Compact specifications */
            .key-specs {
                page-break-before: always;
                page-break-inside: avoid;
                margin: 5mm 0;
                padding: 10px;
            }
            
            .specs-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
            }
            
            .spec-group {
                padding: 8px;
            }
            
            .spec-group h4 {
                font-size: 9pt;
                margin-bottom: 5px;
            }
            
            .spec-item {
                font-size: 7pt;
                margin: 2px 0;
            }
            
            /* COMPACT IMAGE SECTIONS - NO BLANK PAGES */
            .images-section { 
                page-break-inside: avoid; 
                margin: 2mm 0;
                padding: 3mm;
                background: none !important;
                border: none !important;
                box-shadow: none !important;
            }
            
            .pinout-section {
                page-break-inside: avoid;
                page-break-before: avoid;
                page-break-after: avoid;
                margin: 2mm 0;
                padding: 3mm;
            }
            
            .pinout-image-large {
                max-width: 170mm !important;
                max-height: 110mm !important;
                height: auto;
                page-break-inside: avoid;
                display: block;
                margin: 2mm auto;
            }
            
            .dimensions-section {
                page-break-inside: avoid;
                page-break-before: avoid;
                margin: 2mm 0;
                padding: 3mm;
            }
            
            .dimensions-image-large {
                max-width: 150mm !important;
                max-height: 90mm !important;
                height: auto;
                page-break-inside: avoid;
                display: block;
                margin: 2mm auto;
            }
            
            /* EXTRA COMPACT PRODUCT VIEWS */
            .product-views-section {
                page-break-inside: avoid;
                margin: 2mm 0;
                padding: 2mm;
            }
            
            .product-views-grid {
                grid-template-columns: 1fr 1fr;
                gap: 5mm;
            }
            
            .product-view-image {
                width: 60mm !important;
                height: 50mm !important;
                object-fit: contain !important;
                object-position: center !important;
                background: white !important;
                padding: 2mm !important;
            }
            
            .view-card {
                padding: 2mm;
                page-break-inside: avoid;
                background: none !important;
                box-shadow: none !important;
            }
            
            /* COMPACT ADDITIONAL DOCS */
            .additional-docs-section {
                page-break-inside: avoid;
                margin: 2mm 0;
                padding: 2mm;
            }
            
            .additional-docs-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 3mm;
            }
            
            .doc-card {
                padding: 2mm;
                page-break-inside: avoid;
                background: none !important;
                box-shadow: none !important;
            }
            
            .topology-image {
                max-width: 70mm !important;
                max-height: 70mm !important;
                height: auto;
            }
            
            /* COMPACT PRODUCT DETAILS */
            .product-details-section {
                page-break-inside: avoid;
                margin: 2mm 0;
                padding: 2mm;
            }
            
            .product-details-grid {
                grid-template-columns: repeat(3, 1fr);
                gap: 2mm;
            }
            
            .detail-card {
                padding: 1.5mm;
                page-break-inside: avoid;
                background: none !important;
                box-shadow: none !important;
            }
            
            .detail-image {
                max-width: 35mm !important;
                max-height: 35mm !important;
                height: auto;
            }
            
            /* Compact tables */
            .table-section { 
                page-break-inside: avoid; 
                margin: 4mm 0;
            }
            
            .section-title {
                font-size: 14pt;
                margin: 6px 0 6px 0;
                padding: 6px 12px;
            }
            
            .professional-table {
                font-size: 10pt;
                page-break-inside: avoid;
                margin: 6px 0;
            }
            
            .professional-table th {
                padding: 6px 4px;
                font-size: 11pt !important;
            }
            
            .professional-table td {
                padding: 4px;
                font-size: 10pt !important;
            }
            
            /* Compact features */
            .features-section { 
                page-break-inside: avoid; 
                page-break-after: avoid !important;
                margin: 4mm 0;
                padding: 8px;
            }
            
            .features-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 6px;
                margin: 8px 0;
            }
            
            .feature-card {
                padding: 6px;
            }
            
            .feature-title {
                font-size: 10pt;
                margin-bottom: 3px;
            }
            
            .feature-desc {
                font-size: 9pt;
                line-height: 1.3;
            }
            
            /* Compact applications */
            .applications-section { 
                page-break-inside: avoid;
                page-break-before: avoid !important; 
                margin: 4mm 0;
                padding: 8px;
            }
            
            .applications-grid {
                grid-template-columns: repeat(3, 1fr);
                gap: 6px;
                margin: 8px 0;
            }
            
            .app-card {
                padding: 6px;
                font-size: 9pt;
            }
            
            .app-title {
                font-size: 10pt;
                margin-bottom: 2px;
            }
            
            /* Compact additional sections */
            .additional-docs-section {
                page-break-inside: avoid;
                margin: 3mm 0;
                padding: 8px;
            }
            
            .additional-docs-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
            }
            
            .doc-card {
                padding: 8px;
            }
            
            .doc-title {
                font-size: 9pt;
                margin-bottom: 5px;
            }
            
            .topology-image {
                max-width: 120mm !important;
                height: auto;
            }
            
            /* Preserve links in PDF */
            .image-link {
                display: inline-block !important;
                text-decoration: none !important;
            }
            
            .product-details-section {
                page-break-inside: avoid;
                margin: 3mm 0;
                padding: 8px;
            }
            
            .product-details-grid {
                grid-template-columns: repeat(3, 1fr);
                gap: 6px;
            }
            
            .detail-card {
                padding: 6px;
            }
            
            .detail-title {
                font-size: 8pt;
                margin-bottom: 4px;
            }
            
            .detail-image {
                max-width: 100px;
            }
            
            .detail-caption {
                font-size: 6pt;
            }
            
            /* Compact footer */
            .footer {
                page-break-inside: avoid;
                margin-top: 8mm;
                padding: 8px 15px;
            }
            
            .footer-grid {
                font-size: 7pt;
            }
            
            .footer-center {
                font-size: 8pt;
            }
            
            /* Remove excessive spacing */
            .page-section {
                min-height: auto;
                page-break-inside: auto;
            }
            
            /* Ensure sections flow together */
            .section-header {
                page-break-after: avoid;
                margin-bottom: 8px;
                padding-bottom: 4px;
                font-size: 11pt;
            }
            
            .pinout-caption, .dimensions-caption {
                font-size: 8pt;
                margin-top: 5px;
            }
            
            .view-caption, .doc-caption {
                font-size: 7pt;
                margin-top: 3px;
            }
            
            /* Remove hover effects */
            .image-card:hover,
            .feature-card:hover,
            .professional-table tbody tr:hover,
            .view-card:hover,
            .detail-card:hover {
                transform: none !important;
                box-shadow: initial !important;
            }
        }
        
        /* COMPACT LAYOUT OPTIMIZATIONS */
        .pinout-section, .dimensions-section {
            margin: 15px 0;
            padding: 15px;
        }
        
        .product-views-section {
            margin: 15px 0;
        }
        
        .additional-docs-section, .product-details-section {
            margin: 15px 0;
        }
        
        /* Reduce excessive spacing */
        .section-header {
            margin-bottom: 15px;
            margin-top: 10px;
        }
        
        .view-card, .doc-card, .detail-card {
            margin-bottom: 15px;
        }
        
        /* Compact grid layouts */
        .product-views-grid {
            gap: 15px;
        }
        
        .additional-docs-grid, .product-details-grid {
            gap: 15px;
        }
        
        /* Optimize image containers */
        .pinout-container, .dimensions-container {
            margin: 10px 0;
        }
        
        .pinout-caption, .dimensions-caption, .view-caption, .doc-caption, .detail-caption {
            margin-top: 8px;
            margin-bottom: 5px;
        }
        
        /* RESPONSIVE IMAGE STYLES FOR WEB AND PRINT */
        .pinout-image-large {
            width: 100%;
            max-width: 900px;
            height: auto;
            object-fit: contain;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            background: white;
            padding: 10px;
            display: block;
            margin: 0 auto;
        }
        
        .dimensions-image-large {
            width: 100%;
            max-width: 800px;
            height: auto;
            object-fit: contain;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            background: white;
            padding: 10px;
            display: block;
            margin: 0 auto;
        }
        
        .product-view-image {
            width: 100%;
            max-width: 350px;
            min-width: 300px;
            height: 250px;
            object-fit: contain;
            object-position: center;
            border-radius: 6px;
            background: white;
            padding: 8px;
            display: block;
            margin: 0 auto;
        }
        
        .topology-image {
            width: 100%;
            max-width: 650px;
            height: auto;
            object-fit: contain;
            border-radius: 6px;
            background: white;
            padding: 8px;
            display: block;
            margin: 0 auto;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .topology-image:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* Estilo para enlaces de imágenes */
        .image-link {
            display: inline-block;
            text-decoration: none;
            border: none;
        }
        
        .image-link:hover .topology-image {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* TOPOLOGY SECTION - STANDALONE WITH LARGE IMAGE */
        .topology-section {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            page-break-inside: avoid;
        }
        
        .topology-image-large {
            width: 100%;
            max-width: 800px;
            height: auto;
            object-fit: contain;
            border-radius: 8px;
            background: white;
            padding: 15px;
            display: block;
            margin: 0 auto;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid #e2e8f0;
        }
        
        .topology-image-large:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        /* SCHEMATIC SECTION - STANDALONE WITH PAGE BREAK */
        .schematic-section {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            page-break-before: always;
            page-break-inside: avoid;
        }
        
        .schematic-image {
            width: 100%;
            max-width: 300px;
            height: auto;
            object-fit: contain;
            border-radius: 8px;
            background: white;
            padding: 15px;
            display: block;
            margin: 0 auto;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid #e2e8f0;
        }
        
        .schematic-image:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        .detail-image {
            width: 100%;
            max-width: 250px;
            height: auto;
            object-fit: contain;
            border-radius: 6px;
            background: white;
            padding: 8px;
            display: block;
            margin: 0 auto;
        }
        
        /* PDF placeholder styles */
        .pdf-placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 120px;
            background: #f8f9fa;
            border: 2px dashed #6c757d;
            border-radius: 8px;
            text-align: center;
            max-width: 250px;
            margin: 0 auto;
        }
        
        .pdf-icon {
            font-size: 32px;
            margin-bottom: 8px;
        }
        
        .pdf-text {
            font-weight: bold;
            color: #495057;
            margin-bottom: 8px;
        }
        
        .pdf-link {
            background: #007bff;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 12px;
            transition: background-color 0.3s;
        }
        
        .pdf-link:hover {
            background: #0056b3;
            color: white;
        }
        }
        
        /* IMAGE CONTAINERS */
        .pinout-container, .dimensions-container {
            text-align: center;
            margin: 15px 0;
        }
        
        .product-views-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .additional-docs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .product-details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        /* PREVENT ORPHANED HEADERS AND EMPTY SECTIONS */
            h1, h2, h3, h4, .images-title, .section-title, .section-title-major, .section-header {
                page-break-after: avoid;
                page-break-inside: avoid;
                orphans: 3;
                widows: 3;
            }
            
            .view-title, .doc-title, .detail-title {
                font-size: 8pt;
                margin: 1mm 0;
                page-break-after: avoid;
            }
            
            /* HIDE EMPTY SECTIONS COMPLETELY */
            .visual-section:empty,
            .images-section:empty,
            .product-views-section:empty,
            .additional-docs-section:empty,
            .product-details-section:empty {
                display: none !important;
            }
            
            /* ENSURE CONTINUOUS FLOW */
            .section-title-major {
                font-size: 13pt;
                margin: 3mm 0 2mm 0;
                padding: 1mm 0;
                page-break-after: avoid;
            }
            
            /* FORCE ALL VISUAL CONTENT TO STICK TOGETHER */
            .visual-section .images-section:first-child {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            .images-section + .pinout-section,
            .pinout-section + .dimensions-section,
            .dimensions-section + .product-views-section,
            .product-views-section + .additional-docs-section,
            .additional-docs-section + .product-details-section {
                page-break-before: avoid !important;
                margin-top: 2mm !important;
            }
        
        /* PINOUT PAGE STYLES - OPTIMIZED FOR A4 */
        .pinout-page {
            page-break-before: always;
            page-break-after: avoid;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        .pinout-page-title {
            font-size: 28pt;
            font-weight: bold;
            color: #374151;
            text-align: center;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .pinout-page-subtitle {
            font-size: 16pt;
            color: #475569;
            text-align: center;
            margin-bottom: 30px;
            font-style: italic;
        }
        
        .pinout-page-container {
            width: 100%;
            max-width: 95%;
            text-align: center;
            margin: 20px auto;
            overflow: hidden;
        }
        
        .pinout-page-image {
            width: 100%;
            max-width: 100%;
            height: auto;
            object-fit: contain;
            border-radius: 12px;
            background: white;
            padding: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            box-sizing: border-box;
        }
        
        .pinout-page-caption {
            font-size: 14pt;
            color: #374151;
            text-align: center;
            margin-top: 20px;
            font-weight: 500;
            line-height: 1.5;
        }
        
        /* A4 PRINT OPTIMIZATION FOR PINOUT */
        @media print {
            .pinout-page {
                width: 210mm !important;
                height: auto !important;
                margin: 0 !important;
                padding: 8mm !important;
                page-break-before: always !important;
                page-break-after: avoid !important;
                page-break-inside: avoid !important;
                box-sizing: border-box !important;
                background: white !important;
            }
            
            .pinout-page-container {
                max-width: 194mm !important;
                width: 194mm !important;
                margin: 0 auto !important;
                box-sizing: border-box !important;
                overflow: visible !important;
            }
            
            .pinout-page-image {
                max-width: 194mm !important;
                width: 194mm !important;
                max-height: 250mm !important;
                height: auto !important;
                object-fit: contain !important;
                display: block !important;
                margin: 0 auto !important;
                box-sizing: border-box !important;
                padding: 5mm !important;
            }
            
            .pinout-page-title {
                font-size: 24pt !important;
                margin-bottom: 8px !important;
            }
            
            .pinout-page-subtitle {
                font-size: 14pt !important;
                margin-bottom: 15px !important;
            }
            
            .pinout-page-caption {
                font-size: 12pt !important;
                margin-top: 10px !important;
            }
        }
        
        /* PIN DESCRIPTION PAGE - SEPARATE PAGE FOR TABLE */
        .pin-description-page {
            page-break-before: always;
            page-break-after: avoid;
            min-height: 100vh;
            padding: 40px;
            background: white;
        }
        
        /* PINOUT LAYOUT PAGE - SEPARATE PAGE FOR IMAGE */
        .pinout-layout-page {
            page-break-before: always;
            page-break-after: avoid;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        /* A4 PRINT OPTIMIZATION FOR NEW PIN PAGES */
        @media print {
            .pin-description-page {
                width: 210mm !important;
                height: auto !important;
                margin: 0 !important;
                padding: 15mm !important;
                page-break-before: always !important;
                page-break-after: avoid !important;
                page-break-inside: avoid !important;
                box-sizing: border-box !important;
                background: white !important;
            }
            
            .pinout-layout-page {
                width: 210mm !important;
                height: auto !important;
                margin: 0 !important;
                padding: 8mm !important;
                page-break-before: always !important;
                page-break-after: avoid !important;
                page-break-inside: avoid !important;
                box-sizing: border-box !important;
                background: white !important;
            }
        }
        
        /* OVERRIDE ALL FONT SIZES FOR PRINT */
        @media print {
            .specs-title {
                font-size: 18pt !important;
            }
            
            .spec-group h4 {
                font-size: 14pt !important;
            }
            
            .spec-item {
                font-size: 12pt !important;
            }
            
            .section-title {
                font-size: 14pt !important;
            }
            
            .feature-title {
                font-size: 10pt !important;
            }
            
            .feature-desc {
                font-size: 9pt !important;
            }
            
            .app-title {
                font-size: 10pt !important;
            }
            
            .app-card {
                font-size: 9pt !important;
            }
        }
        
        /* INTRODUCTION SECTION - ESPACIADO COMPACTO */
        .introduction-section {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .introduction-content {
            font-size: 11pt;
            line-height: 1.6;
            color: #374151;
            text-align: justify;
        }
        
        .introduction-content p {
            margin: 8px 0;
            color: #374151;
            line-height: 1.6;
        }
        
        /* PRODUCT VIEWS SECTION - EARLY PLACEMENT */
        .product-views-section {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .product-views-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 15px 0;
        }
        
        .view-card {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        .view-title {
            font-size: 12pt;
            font-weight: bold;
            color: #374151;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .product-view-image {
            width: 100%;
            max-width: 300px;
            min-width: 250px;
            height: 200px;
            object-fit: contain;
            object-position: center;
            border-radius: 6px;
            background: white;
            padding: 8px;
            display: block;
            margin: 0 auto;
        }
        
        .view-caption {
            font-size: 9pt;
            color: #6b7280;
            margin-top: 8px;
            font-style: italic;
        }
        
        /* SCHEMATIC LINK STYLES */
        .doc-link {
            margin-top: 10px;
            text-align: center;
        }
        
        .schematic-link {
            display: inline-block;
            background: #374151;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 12pt;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 2px solid #374151;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .schematic-link:hover {
            background: white;
            color: #374151;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* ESTILOS ESPECÍFICOS PARA VISUALIZACIÓN WEB */
        @media screen {
            body {
                background: #f8fafc;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                background: white;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                border-radius: 12px;
                overflow: hidden;
            }
            
            .header {
                border-bottom: 3px solid #e5e7eb;
            }
            
            .key-specs {
                margin: 20px;
                border: 1px solid #e5e7eb;
            }
            
            .images-section {
                margin: 20px;
                border: 1px solid #e5e7eb;
            }
            
            .visual-content {
                margin: 20px;
                padding: 20px;
                background: #f9fafb;
                border-radius: 8px;
            }
            
            .pin-description-page {
                margin: 20px;
                padding: 30px;
                background: white;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                min-height: auto;
                page-break-before: unset;
                page-break-after: unset;
            }
            
            .pinout-layout-page {
                margin: 20px;
                padding: 30px;
                background: white;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                min-height: auto;
                page-break-before: unset;
                page-break-after: unset;
            }
            
            .pinout-page {
                margin: 20px;
                padding: 30px;
                background: white;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                min-height: auto;
                page-break-before: unset;
                page-break-after: unset;
            }
            
            /* Estilos específicos para títulos de pinout en web */
            .pinout-page-title {
                font-size: 24pt !important;
                color: #374151 !important;
                text-align: center !important;
                margin-bottom: 15px !important;
                padding-bottom: 10px !important;
                border-bottom: 2px solid #374151 !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
            }
            
            .pinout-page-subtitle {
                font-size: 14pt !important;
                color: #6b7280 !important;
                text-align: center !important;
                margin-bottom: 25px !important;
                font-style: italic !important;
            }
            
            .pinout-table-section {
                margin: 20px 0 !important;
            }
            
            .pinout-page-container {
                text-align: center !important;
                margin: 20px auto !important;
                max-width: 800px !important;
                width: 100% !important;
            }
            
            .pinout-page-image {
                width: 100% !important;
                max-width: 100% !important;
                height: auto !important;
                border-radius: 8px !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                background: white !important;
                padding: 15px !important;
                object-fit: contain !important;
                display: block !important;
                margin: 0 auto !important;
            }
            
            .pinout-page-caption {
                font-size: 12pt !important;
                color: #374151 !important;
                text-align: center !important;
                margin-top: 15px !important;
                line-height: 1.5 !important;
                font-style: italic !important;
            }
            
            .professional-table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                font-size: 11pt;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-radius: 6px;
                overflow: hidden;
            }
            
            .professional-table th {
                background: #374151;
                color: white;
                padding: 12px 15px;
                font-weight: 600;
                text-align: left;
                border-bottom: 2px solid #4b5563;
            }
            
            .professional-table td {
                padding: 10px 15px;
                border-bottom: 1px solid #e5e7eb;
                background: white;
            }
            
            .professional-table tr:nth-child(even) td {
                background: #f9fafb;
            }
            
            .professional-table tr:hover td {
                background: #f3f4f6;
            }
            
            /* Estilos específicos para tablas de pinout */
            .pinout-table {
                margin: 20px auto !important;
                max-width: 800px !important;
            }
            
            .pinout-table th {
                background: #1f2937 !important;
                color: white !important;
                font-size: 12pt !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }
            
            .pin-number {
                color: #374151 !important;
                padding: 4px 8px !important;
                font-weight: bold !important;
                text-align: center !important;
                display: inline-block !important;
            }
            
            .pin-name {
                font-weight: 600 !important;
                color: #1f2937 !important;
                font-family: 'Courier New', monospace !important;
            }
            
            .pin-function {
                color: #374151 !important;
            }
            
            .download-button {
                position: fixed;
                top: 20px;
                right: 20px;
                background: #374151;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 500;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                z-index: 1000;
                transition: all 0.3s ease;
            }
            
            .download-button:hover {
                background: #1f2937;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
            
            .section-title-major {
                font-size: 20pt;
                margin: 30px 0 20px 0;
                padding: 15px 0;
                border-bottom: 2px solid #374151;
                color: #374151;
            }
            
            .section-header {
                font-size: 16pt;
                margin: 20px 0 15px 0;
                color: #374151;
                font-weight: 600;
            }
            
            /* Mejorar espaciado y legibilidad */
            .introduction-section {
                margin: 20px;
                padding: 25px;
                background: white;
                border-radius: 8px;
                border-left: 4px solid #374151;
            }
            
            .product-views {
                margin: 20px;
                padding: 20px;
                background: #f9fafb;
                border-radius: 8px;
            }
            
            .applications-section {
                margin: 20px;
                padding: 20px;
                background: white;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }
            
            /* Mejorar la estructura general del documento */
            .section-title {
                font-size: 18pt !important;
                color: #374151 !important;
                margin: 25px 0 15px 0 !important;
                padding-bottom: 8px !important;
                border-bottom: 2px solid #e5e7eb !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }
            
            .section-title-major {
                font-size: 22pt !important;
                color: #1f2937 !important;
                margin: 30px 0 20px 0 !important;
                padding: 15px 0 10px 0 !important;
                border-bottom: 3px solid #374151 !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
                text-align: center !important;
            }
            
            .section-header {
                font-size: 16pt !important;
                color: #374151 !important;
                margin: 20px 0 15px 0 !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
            }
            
            /* Espaciado consistente para todas las secciones */
            .introduction-section,
            .product-views-section,
            .visual-content > div,
            .pin-description-page,
            .pinout-layout-page {
                margin-bottom: 20px !important;
            }
            
            /* Mejorar navegación y interactividad */
            .image-card {
                cursor: pointer;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .image-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }
            
            .no-print {
                display: block !important;
            }
        }
        
        /* ESTILOS PARA IMPRESIÓN - OCULTAR ELEMENTOS WEB */
        @media print {
            .no-print {
                display: none !important;
            }
            
            .download-button {
                display: none !important;
            }
            
            body {
                background: white !important;
                padding: 0 !important;
            }
            
            .container {
                max-width: none !important;
                box-shadow: none !important;
                border-radius: 0 !important;
                background: white !important;
            }
        }
        """
    def parse_readme(self, readme_path):
        """Parsea README y extrae información técnica"""
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Limpiar comentarios
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Extraer frontmatter
        frontmatter = {}
        frontmatter_match = re.match(r'^---(.*?)---', content, re.DOTALL)
        if frontmatter_match:
            try:
                frontmatter = yaml.safe_load(frontmatter_match.group(1))
                content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
            except:
                pass
        
        return {
            'frontmatter': frontmatter,
            'content': content,
            'date': datetime.now(ZoneInfo("America/Mexico_City")).strftime("%Y-%m-%d")
        }

    def parse_hardware_readme(self):
        """Parsea el README de hardware si existe"""
        # Intentar múltiples rutas posibles para el README de hardware
        possible_paths = [
            "../../hardware/README.md",  # Desde software/documentation
            "../../../hardware/README.md",  # Por si está en otro nivel
            "./hardware/README.md",  # En el mismo directorio
            "../hardware/README.md"  # Un nivel arriba
        ]
        
        for relative_path in possible_paths:
            hardware_readme_path = os.path.abspath(os.path.join(self.base_path, relative_path))
            if os.path.exists(hardware_readme_path):
                print(f"📖 Found hardware README: {hardware_readme_path}")
                return self.parse_readme(hardware_readme_path)
        
        print("⚠️ Hardware README not found in any expected location")
        return None

    def combine_readme_content(self, main_data, hardware_data):
        """Combina información de README principal y hardware"""
        if not hardware_data:
            return main_data
        
        combined_content = main_data['content']
        hardware_content = hardware_data['content']
        
        # Extraer secciones útiles del hardware README
        hardware_sections = {
            'Pinout': self.extract_section('Pinout', hardware_content),
            'Description': self.extract_section('Description', hardware_content),
            'Dimensions': self.extract_section('Dimensions', hardware_content),
            'Topology': self.extract_section('Topology', hardware_content)
        }
        
        # Buscar tabla de componentes/referencias
        component_table = self.extract_component_table(hardware_content)
        
        # Extraer tabla de pinout detallada del hardware
        pinout_table = self.extract_pinout_table(hardware_content)
        
        # Agregar información de hardware que no esté en el README principal
        if pinout_table and 'Pin & Connector Layout' not in combined_content:
            combined_content += f"\n\n## Pin & Connector Layout\n{pinout_table}"
        elif hardware_sections['Pinout'] and 'Pinout' not in combined_content:
            combined_content += f"\n\n## Pin & Connector Layout\n{hardware_sections['Pinout']}"
        
        if component_table:
            combined_content += f"\n\n## Component Reference\n{component_table}"
        
        # Combinar frontmatter si existe
        combined_frontmatter = main_data['frontmatter'].copy()
        if hardware_data['frontmatter']:
            combined_frontmatter.update(hardware_data['frontmatter'])
        
        return {
            'frontmatter': combined_frontmatter,
            'content': combined_content,
            'date': main_data['date'],
            'hardware_data': hardware_data
        }

    def extract_pinout_table(self, content):
        """Extrae tabla de pinout del hardware README"""
        lines = content.split('\n')
        table_started = False
        table_lines = []
        in_pinout_section = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # Detectar si estamos en la sección de pinout
            if line_stripped.lower().startswith('## pinout') or line_stripped.lower().startswith('### description'):
                in_pinout_section = True
                continue
            
            # Si estamos en la sección correcta y encontramos una tabla
            if in_pinout_section and '|' in line_stripped:
                if not table_started:
                    # Verificar si es una tabla de pinout
                    if any(keyword in line_stripped.lower() for keyword in ['pin', 'signal', 'description']):
                        table_started = True
                        table_lines.append(line_stripped)
                else:
                    table_lines.append(line_stripped)
            elif table_started and line_stripped.startswith('##'):
                break
            elif table_started and line_stripped == '---':
                break
        
        if table_lines and len(table_lines) >= 3:  # Header, separator, and at least one data row
            return '\n'.join(table_lines)
        
        return None

    def extract_component_table(self, content):
        """Extrae tabla de componentes del hardware README"""
        lines = content.split('\n')
        table_started = False
        table_lines = []
        in_table_section = False
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Detectar si estamos después de una sección Topology
            if line_stripped.lower().startswith('## topology'):
                in_table_section = True
                continue
            
            # Si estamos en la sección correcta y encontramos una tabla
            if in_table_section and '|' in line_stripped:
                if not table_started:
                    # Verificar si es una tabla de componentes/referencias
                    if any(keyword in line_stripped.lower() for keyword in ['ref', 'description', 'component']):
                        table_started = True
                        table_lines.append(line_stripped)
                else:
                    table_lines.append(line_stripped)
            elif table_started and line_stripped == '---':
                break
            elif table_started and not line_stripped and len(table_lines) > 2:
                break
        
        if table_lines and len(table_lines) >= 3:  # Header, separator, and at least one data row
            return '\n'.join(table_lines)
        
        return None

    def extract_section(self, heading, content):
        """Extrae sección específica"""
        pattern = rf'##+\s*{re.escape(heading)}\s+(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def find_hardware_images(self):
        """Encuentra imágenes de hardware con patrones genéricos"""
        images = {
            'unit_top': None,
            'unit_bottom': None,
            'unit_pinout': None,
            'unit_dimensions': None,
            'unit_topology': None,
            'unit_schematic': None
        }
        
        # Buscar archivos en hardware/resources con rutas absolutas
        hardware_abs_path = os.path.abspath(self.hardware_path)
        
        if os.path.exists(hardware_abs_path):
            for file in os.listdir(hardware_abs_path):
                file_lower = file.lower()
                
                # Solo procesar archivos de imagen
                if not any(file_lower.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
                    continue
                
                # Mapear archivos por patrones genéricos usando solo el nombre de archivo
                if any(pattern in file_lower for pattern in ['topology', 'block_diagram', 'system']):
                    images['unit_topology'] = file
                elif any(pattern in file_lower for pattern in ['_top', 'top_view', 'topview']) and 'topology' not in file_lower:
                    images['unit_top'] = file
                elif any(pattern in file_lower for pattern in ['_btm', '_bottom', 'bottom_view', 'bottomview']):
                    images['unit_bottom'] = file
                elif any(pattern in file_lower for pattern in ['pinout', 'pin_out', 'pins', 'pinmap']):
                    # Preferir PNG sobre JPG, luego inglés sobre español
                    current_pinout = images['unit_pinout']
                    should_replace = False
                    
                    if not current_pinout:
                        should_replace = True
                    elif file.lower().endswith('.png') and current_pinout.lower().endswith('.jpg'):
                        should_replace = True  # Preferir PNG sobre JPG
                    elif 'en' in file_lower and 'es' in current_pinout.lower():
                        should_replace = True  # Preferir inglés sobre español
                    elif file.lower().endswith('.png') and current_pinout.lower().endswith('.png') and 'en' in file_lower:
                        should_replace = True  # Entre PNGs, preferir inglés
                    
                    if should_replace:
                        images['unit_pinout'] = file
                elif any(pattern in file_lower for pattern in ['dimension', 'dimensions', 'size', 'mechanical']):
                    images['unit_dimensions'] = file
                elif any(pattern in file_lower for pattern in ['sch', 'schematic', 'circuit']):
                    # Detectar esquemáticos tanto en imagen como en PDF
                    images['unit_schematic'] = file
        
        return images

    def extract_electrical_specs_from_discovery(self, discovered_data):
        """Extrae especificaciones eléctricas desde los datos descubiertos"""
        specs = {}
        connectivity = {}
        
        # Buscar en múltiples secciones posibles
        spec_sections = discovered_data['explorer'].get_best_section([
            'Key Features', 'Features', 'Specifications', 
            'Technical Specifications', 'Electrical Characteristics'
        ])
        
        if spec_sections:
            content = spec_sections['content']
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith('- ') and ':' in line:
                    clean_line = line[2:].strip()
                    if ':' in clean_line:
                        key, value = clean_line.split(':', 1)
                        key_clean = key.strip().replace('**', '')
                        value_clean = value.strip()
                        
                        # Mapear especificaciones técnicas
                        if any(term in key_clean.lower() for term in ['axes', 'axis']):
                            specs['Measurement Axes'] = value_clean
                        elif any(term in key_clean.lower() for term in ['range', 'measurement range']):
                            specs['Measurement Range'] = value_clean
                        elif 'resolution' in key_clean.lower():
                            specs['Resolution'] = value_clean
                        elif any(term in key_clean.lower() for term in ['power', 'consumption']):
                            specs['Power Consumption'] = value_clean
                        elif any(term in key_clean.lower() for term in ['voltage', 'supply']):
                            specs['Operating Voltage'] = value_clean
                        elif 'temperature' in key_clean.lower():
                            specs['Operating Temperature'] = value_clean
                        elif 'interface' in key_clean.lower():
                            connectivity['interfaces'] = value_clean
                        else:
                            specs[key_clean] = value_clean
        
        # Valores por defecto genéricos si no se encuentra información
        if not specs:
            specs = {
                'Operating Voltage': '3.3V typical',
                'Power Consumption': 'Low power design',
                'Operating Temperature': 'Industrial range'
            }
        
        if not connectivity:
            connectivity = {
                'interfaces': 'Digital communication',
                'connector': 'Standard connectors'
            }
        
        return specs, connectivity

    def extract_features_from_discovery(self, discovered_data):
        """Extrae características desde los datos descubiertos"""
        features = []
        
        # Buscar sección de características
        features_section = discovered_data['explorer'].get_best_section([
            'Key Features', 'Features', 'Main Features', 'Technical Features'
        ])
        
        if features_section:
            content = features_section['content']
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith('- '):
                    feature = line[2:].strip().replace('**', '')
                    
                    if ':' in feature:
                        title, desc = feature.split(':', 1)
                        features.append({
                            'title': title.strip(),
                            'desc': desc.strip(),
                            'icon': ''
                        })
                    else:
                        features.append({
                            'title': feature,
                            'desc': '',
                            'icon': ''
                        })
        
        return features

    def extract_introduction_from_discovery(self, discovered_data):
        """Extrae introducción desde los datos descubiertos sin duplicados"""
        paragraphs = []
        
        # Leer directamente el README principal
        main_readme_path = os.path.join(self.repo_root, 'README.md')
        try:
            if os.path.exists(main_readme_path):
                with open(main_readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraer solo la sección Introduction
                lines = content.split('\n')
                in_intro_section = False
                intro_lines = []
                
                for line in lines:
                    if line.strip() == '## Introduction':
                        in_intro_section = True
                        continue
                    elif line.startswith('## ') and in_intro_section:
                        # Nueva sección, terminar
                        break
                    elif in_intro_section:
                        # Filtrar líneas de HTML/markdown
                        if (not line.strip().startswith('<') and 
                            not line.strip().startswith('!') and
                            line.strip() != ''):
                            intro_lines.append(line)
                
                if intro_lines:
                    # Unir las líneas y limpiar
                    intro_text = '\n'.join(intro_lines).strip()
                    # Limpiar markdown básico
                    intro_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', intro_text)
                    intro_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', intro_text)
                    
                    if intro_text:
                        paragraphs.append(intro_text)
                        
        except Exception as e:
            print(f"⚠️ Error al leer README: {e}")
        
        # Fallback si no se encontró contenido
        if not paragraphs:
            paragraphs = [
                "Professional electronic module designed for reliable performance and easy integration with modern development platforms."
            ]
        
        return paragraphs

    def extract_tables_from_discovery(self, discovered_data):
        """Extrae todas las tablas desde los datos descubiertos y las clasifica por tipo"""
        all_tables = []
        
        # Usar el explorer para buscar secciones con tablas
        if 'explorer' in discovered_data and hasattr(discovered_data['explorer'], 'sections'):
            sections = discovered_data['explorer'].sections
            
            for section_name, section_data in sections.items():
                content_text = section_data.get('content', '')
                if not content_text:
                    continue
                
                # Buscar tablas en el contenido
                tables = self.extract_tables_from_text(content_text)
                for table in tables:
                    all_tables.append({
                        'source_section': section_name,
                        'data': table
                    })
        
        # También buscar en las secciones principales
        sections = discovered_data.get('sections', {})
        for section_name, section_content in sections.items():
            # Verificar si section_content es un diccionario o una cadena
            if isinstance(section_content, dict):
                content_text = section_content.get('content', section_content.get('text', ''))
            else:
                content_text = section_content
            
            if not content_text:
                continue
            
            tables = self.extract_tables_from_text(content_text)
            for table in tables:
                all_tables.append({
                    'source_section': section_name,
                    'data': table
                })
        
        return all_tables

    def extract_markdown_table(self, content):
        """Extrae tabla markdown de contenido"""
        if not content.strip():
            return None
            
        table_pattern = r'(\|.*\n)+'
        table_match = re.search(table_pattern, content)
        if not table_match:
            return None
            
        lines = [line.strip() for line in table_match.group(0).strip().split('\n') if '|' in line]
        if len(lines) < 2:
            return None
            
        return '\n'.join(lines)

    def extract_features_detailed(self, content):
        """Extrae características con más detalle"""
        features_section = self.extract_section('Key Features', content)
        features = []
        
        if features_section:
            lines = features_section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- '):
                    feature = line[2:].strip()
                    # Eliminar markdown formatting
                    feature = feature.replace('**', '')
                    
                    if ':' in feature:
                        title, desc = feature.split(':', 1)
                        features.append({
                            'title': title.strip(),
                            'desc': desc.strip(),
                            'icon': ''
                        })
                    else:
                        features.append({
                            'title': feature,
                            'desc': '',
                            'icon': ''
                        })
        
        # Si no se encontraron features en Key Features, buscar en otras secciones
        if not features:
            # Intentar extraer de sección Features
            alt_features_section = self.extract_section('Features', content)
            if alt_features_section:
                lines = alt_features_section.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('- '):
                        feature = line[2:].strip().replace('**', '')
                        if ':' in feature:
                            title, desc = feature.split(':', 1)
                            features.append({
                                'title': title.strip(),
                                'desc': desc.strip(),
                                'icon': ''
                            })
                        else:
                            features.append({
                                'title': feature,
                                'desc': '',
                                'icon': ''
                            })
        
        return features

    def extract_key_features(self, content):
        """Extrae características clave desde la sección Features para mostrar en la tabla de especificaciones"""
        features_section = self.extract_section('Features', content)
        key_features = {}
        
        if features_section:
            lines = features_section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- ') and ':' in line:
                    # Formato "- Característica: valor"
                    clean_line = line[2:].strip()  # Quitar el guión
                    if ':' in clean_line:
                        key, value = clean_line.split(':', 1)
                        key_clean = key.strip()
                        value_clean = value.strip()
                        
                        # Solo tomar características técnicas clave (no interfaces que ya están en conectividad)
                        if not any(word in key_clean.lower() for word in ['interface', 'connector', 'form', 'factor']):
                            # Simplificar nombres para la tabla
                            if 'temperature' in key_clean.lower():
                                key_features['Temperature'] = value_clean
                            elif 'humidity' in key_clean.lower():
                                key_features['Humidity'] = value_clean
                            elif 'pressure' in key_clean.lower() or 'barometric' in key_clean.lower():
                                key_features['Pressure'] = value_clean
                            elif 'voc' in key_clean.lower() or 'gas' in key_clean.lower() or 'air quality' in key_clean.lower():
                                key_features['Gas Detection'] = value_clean
        
        return key_features

    def markdown_table_to_html_professional(self, section_content, table_type='general'):
        """Convierte tabla markdown a HTML profesional"""
        if not section_content.strip():
            return ""
            
        table_pattern = r'(\|.*\n)+'
        table_match = re.search(table_pattern, section_content)
        if not table_match:
            return ""
            
        lines = [line.strip() for line in table_match.group(0).strip().split('\n') if '|' in line]
        if len(lines) < 2:
            return ""
            
        headers = [cell.strip() for cell in lines[0].strip('|').split('|')]
        rows = []
        for line in lines[2:]:
            row = [cell.strip() for cell in line.strip('|').split('|')]
            if len(row) == len(headers):
                rows.append(row)
        
        if not rows:
            return ""
            
        # Determinar clases CSS según el tipo de tabla
        table_class = 'professional-table'
        if table_type == 'pinout':
            table_class += ' pinout-table'
            # Para tablas de pinout, omitir la primera columna (PIN) para evitar duplicación
            headers = headers[1:]  # Omitir primera columna
            rows = [row[1:] for row in rows]  # Omitir primera columna de cada fila
        elif table_type == 'components' and len(headers) == 3 and 'pin' in headers[0].lower():
            # Para tablas de componentes que son realmente pinout, omitir primera columna duplicada
            headers = headers[1:]  # Omitir primera columna
            rows = [row[1:] for row in rows]  # Omitir primera columna de cada fila
        
        html = f'<table class="{table_class}">\n<thead>\n<tr>\n'
        for header in headers:
            html += f'<th>{header}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        
        for i, row in enumerate(rows):
            html += '<tr>\n'
            for j, cell in enumerate(row):
                # Procesar el contenido de la celda según el tipo de tabla
                processed_cell = cell
                
                # Para tablas de aplicaciones/recursos, preservar enlaces como HTML funcional
                if table_type == 'applications':
                    processed_cell = self.convert_markdown_links_to_html(cell)
                else:
                    # Para otras tablas, limpiar enlaces manteniendo solo el texto
                    processed_cell = self.clean_markdown_links(cell)
                
                if table_type == 'pinout':
                    # Primera columna: Signal (nombre de señal) - ahora es la primera después de omitir PIN
                    if j == 0:
                        html += f'<td class="pin-name">{processed_cell}</td>\n'
                    # Segunda columna y siguientes: Description/Function
                    else:
                        html += f'<td class="pin-function">{processed_cell}</td>\n'
                elif table_type == 'components' and len(headers) == 2 and any('signal' in h.lower() for h in headers):
                    # Para tablas de componentes que son realmente pinout
                    if j == 0:
                        html += f'<td class="pin-name">{processed_cell}</td>\n'
                    else:
                        html += f'<td class="pin-function">{processed_cell}</td>\n'
                else:
                    html += f'<td>{processed_cell}</td>\n'
            html += '</tr>\n'
        
        html += '</tbody>\n</table>'
        return html

    def copy_images_to_build(self, images):
        """Copia las imágenes necesarias al directorio build"""
        build_dir = os.path.join(os.path.dirname(__file__), 'build')
        hardware_abs_path = os.path.abspath(self.hardware_path)
        
        # Asegurar que el directorio build existe
        os.makedirs(build_dir, exist_ok=True)
        
        # Copiar logo
        logo_path = os.path.join(os.path.dirname(__file__), 'images', 'logo_unit.png')
        if os.path.exists(logo_path):
            logo_dest_dir = os.path.join(build_dir, 'images')
            os.makedirs(logo_dest_dir, exist_ok=True)
            shutil.copy2(logo_path, os.path.join(logo_dest_dir, 'logo_unit.png'))
            print(f"📋 Copied logo to build/images/")
        
        # Copiar imágenes de hardware que se están usando
        if os.path.exists(hardware_abs_path):
            for image_key, image_file in images.items():
                if image_file:  # Si hay una imagen asignada
                    source_path = os.path.join(hardware_abs_path, image_file)
                    if os.path.exists(source_path):
                        dest_path = os.path.join(build_dir, image_file)
                        shutil.copy2(source_path, dest_path)
                        print(f"📋 Copied {image_file} to build/")
        
        # Copiar PDFs de esquemáticos desde hardware/resources
        if os.path.exists(hardware_abs_path):
            for file in os.listdir(hardware_abs_path):
                if 'sch' in file.lower() and file.lower().endswith('.pdf'):
                    source_path = os.path.join(hardware_abs_path, file)
                    dest_path = os.path.join(build_dir, file)
                    shutil.copy2(source_path, dest_path)
                    print(f"📋 Copied schematic PDF {file} to build/")
        
        # Copiar PDFs de esquemáticos desde hardware/ (directorio padre)
        hardware_parent_path = os.path.dirname(hardware_abs_path)
        if os.path.exists(hardware_parent_path):
            for file in os.listdir(hardware_parent_path):
                if 'sch' in file.lower() and file.lower().endswith('.pdf'):
                    source_path = os.path.join(hardware_parent_path, file)
                    dest_path = os.path.join(build_dir, file)
                    shutil.copy2(source_path, dest_path)
                    print(f"📋 Copied schematic PDF {file} from hardware/ to build/")

    def generate_professional_datasheet(self, readme_path, output_path):
        """Genera hoja de datos profesional completa usando descubrimiento automático"""
        
        # FASE 1: Descubrimiento automático del repositorio
        discovered_data = self.discover_project_information()
        
        # FASE 2: Extraer información usando el nuevo sistema
        metadata = discovered_data['metadata']
        title = metadata.get('title', 'Electronic Module')
        subtitle = metadata.get('subtitle', 'Professional electronic component')
        version = metadata.get('version', '1.0')
        
        # Extraer código del producto de forma genérica mejorada
        product_code = "MODULE"  # Valor por defecto
        
        # Estrategia 1: Buscar en el título patrones específicos (orden de prioridad)
        title_patterns = [
            r'\b([A-Z]{2,4}[0-9]{2,4})\b',  # BMM150, ESP32, BME280, etc. (más específico)
            r'\b(UE\d+)\b',                 # UE0066, etc.
            r'\b([A-Z]{3,}[0-9]+[A-Z]*)\b', # Patrones mixtos más largos
            r'\b([A-Z]{2,}[0-9]+)\b'        # Patrones más generales
        ]
        
        # Buscar primero en el título completo (incluyendo palabras como "Magnetometer BMM150")
        full_title_text = f"{title} {subtitle}"
        
        for i, pattern in enumerate(title_patterns):
            match = re.search(pattern, full_title_text.upper())
            if match:
                candidate = match.group(1)
                # Preferir códigos que no sean palabras comunes
                if candidate not in ['ELECTRONIC', 'MODULE', 'SENSOR', 'UNIT']:
                    product_code = candidate
                    break
        
        # Estrategia 2: Si no se encontró, buscar en el contenido
        if product_code == "MODULE":
            content_combined = discovered_data.get('combined_content', '')
            for pattern in title_patterns:
                match = re.search(pattern, content_combined.upper())
                if match:
                    candidate = match.group(1)
                    if candidate not in ['ELECTRONIC', 'MODULE', 'SENSOR', 'UNIT']:
                        product_code = candidate
                        break
        
        # Estrategia 3: Usar palabras del título como último recurso
        if product_code == "MODULE":
            words = [word.upper() for word in title.split() if word.isalpha() and len(word) > 2]
            # Filtrar palabras comunes
            filtered_words = [w for w in words if w not in ['THE', 'AND', 'FOR', 'WITH', 'ELECTRONIC', 'MODULE']]
            if len(filtered_words) >= 1:
                product_code = filtered_words[0][:6]
            elif len(words) >= 1:
                product_code = words[0][:6]
        
        # FASE 3: Extraer información técnica usando descubrimiento
        images = self.find_hardware_images()
        electrical_specs, connectivity_specs = self.extract_electrical_specs_from_discovery(discovered_data)
        features = self.extract_features_from_discovery(discovered_data)
        introduction_paragraphs = self.extract_introduction_from_discovery(discovered_data)
        tables = self.extract_tables_from_discovery(discovered_data)
        
        # CLASIFICAR TABLAS POR CATEGORÍAS ANTES DE LA GENERACIÓN DEL HTML
        spec_tables = []
        pinout_tables = []
        component_tables = []
        app_tables = []
        
        if tables:
            for table_info in tables:
                section_name = table_info.get('source_section', '').lower()
                table_data = table_info.get('data', [])
                
                # Verificar si es tabla de componentes por el contenido
                is_component_table = False
                if table_data:
                    headers = list(table_data[0].keys()) if table_data else []
                    first_row_values = list(table_data[0].values()) if table_data else []
                    
                    # Si tiene 'Ref' como header o valores como 'IC1', 'U1', etc.
                    if ('ref' in str(headers).lower() or 'reference' in str(headers).lower() or
                        any(str(val).upper().startswith(('IC', 'U', 'R', 'C', 'L', 'SW', 'J', 'JP')) 
                            for val in first_row_values)):
                        is_component_table = True
                
                if 'pinout' in section_name or 'pin' in section_name:
                    pinout_tables.append(table_info)
                elif (is_component_table or 'component' in section_name or 'reference' in section_name or 
                      'ref.' in section_name or section_name.endswith('ref')):
                    component_tables.append(table_info)
                elif 'application' in section_name or 'app' in section_name:
                    app_tables.append(table_info)
                else:
                    spec_tables.append(table_info)
        
        # Convertir listas de especificaciones a formato compatible
        electrical_specs_dict = self.convert_specs_list_to_dict(electrical_specs)
        connectivity_specs_dict = self.convert_specs_list_to_dict(connectivity_specs)
        
        # FASE 4: Extraer aplicaciones
        applications = self.extract_applications_from_discovery(discovered_data)
        
        # Crear fecha
        date = datetime.now(ZoneInfo("America/Mexico_City")).strftime("%Y-%m-%d")
        
        # FASE 5: Crear estructura de datos compatible
        data = {
            'date': date,
            'product_code': product_code,
            'title': title,
            'subtitle': subtitle,
            'version': version
        }
        
        # Obtener contenido combinado para funciones legacy
        content = discovered_data.get('combined_content', '')
        
        # Crear HTML completo
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en" data-product="{product_code}">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} - Professional Technical Datasheet</title>
            <style>{self.css_professional}</style>
        </head>
        <body>
            <a href="#" class="download-button no-print" onclick="window.print()" title="Imprimir o guardar como PDF">
                📄 Descargar PDF
            </a>
            
            <div class="container">
                <!-- HEADER + KEY SPECS -->
                <div class="header">
                    <div class="header-grid">
                        <div class="logo-section">
                            <img src="images/logo_unit.png" alt="UNIT Electronics" class="company-logo" />

                        </div>
                        <div class="product-title-section">
                            <div class="product-code">{product_code}</div>
                            <h1 class="product-title">{title}</h1>
                            <p class="product-subtitle">{subtitle}</p>
                        </div>
                        <div class="version-section">
                            <div class="version-badge">v{version}</div>
                            <div>{data['date']}</div>
                            <div>Rev. A</div>
                        </div>
                    </div>
                </div>
        """
        
        # INTRODUCTION SECTION
        if introduction_paragraphs:
            html += '''
                <div class="introduction-section">
                    <h2 class="section-title">Product Overview</h2>
                    <div class="introduction-content">
            '''
            for paragraph in introduction_paragraphs:
                html += f'<p>{paragraph}</p>'
            html += '''
                    </div>
                </div>
            '''
        
        # PRODUCT VIEWS - Moved here after introduction
        product_views_available = (
            images['unit_top'] or images['unit_bottom']
        )
        
        if product_views_available:
            html += '''
                <div class="product-views-section">
                    <h2 class="section-title">Product Views</h2>
                    <div class="product-views-grid">
            '''
            
            # Top View
            if images['unit_top']:
                html += f'''
                        <div class="view-card">
                            <div class="view-title">TOP VIEW</div>
                            <img src="{images['unit_top']}" alt="Top View" class="product-view-image">
                            <div class="view-caption">Component placement and connectors</div>
                        </div>
                '''
            
            # Bottom View (if available)
            if images['unit_bottom']:
                html += f'''
                        <div class="view-card">
                            <div class="view-title">BOTTOM VIEW</div>
                            <img src="{images['unit_bottom']}" alt="Bottom View" class="product-view-image">
                            <div class="view-caption">Underside components and connections</div>
                        </div>
                '''
            
            html += '''
                    </div>
                </div>
            '''
        
        # KEY SPECIFICATIONS
        if electrical_specs_dict:
            html += '''
                <div class="key-specs">
                    <div class="specs-title">KEY TECHNICAL<br>SPECIFICATIONS</div>
                    <div class="specs-grid">
            '''
            
            # Group specifications
            power_specs = {}
            
            for key, value in electrical_specs_dict.items():
                if any(word in key.lower() for word in ['power', 'supply', 'consumption', 'current', 'voltage']):
                    power_specs[key] = value
            
            if power_specs:
                html += '''
                        <div class="spec-group">
                            <h4>POWER SUPPLY</h4>
                '''
                for key, value in power_specs.items():
                    html += f'''
                            <div class="spec-item">
                                <span class="spec-label">{key}:</span>
                                <span class="spec-value">{value}</span>
                            </div>
                    '''
                html += '</div>'
            
            # Add connectivity specifications
            interfaces = connectivity_specs_dict.get('interfaces', connectivity_specs_dict.get('Interfaces', 'I²C, SPI'))
            connector = connectivity_specs_dict.get('connector', connectivity_specs_dict.get('Connector', 'Qwiic + Pin Headers'))
            html += f'''
                        <div class="spec-group">
                            <h4>CONNECTIVITY</h4>
                            <div class="spec-item">
                                <span class="spec-label">Interfaces:</span>
                                <span class="spec-value">{interfaces}</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Connector:</span>
                                <span class="spec-value">{connector}</span>
                            </div>
                        </div>
                    </div>
                </div>
            '''
        
        # CONTENT FLOWS CONTINUOUSLY - NO SEPARATE SECTIONS
        html += '''
        '''
        
        # PIN CONFIGURATION TABLE
        pinout_table = self.markdown_table_to_html_professional(
            self.extract_section('Pin & Connector Layout', content), 'pinout'
        )
        if pinout_table:
            html += f'''
                    <div class="table-section">
                        <h2 class="section-title">PIN CONFIGURATION</h2>
                        {pinout_table}
                    </div>
            '''
        
        # COMMUNICATION INTERFACES TABLE
        interface_table = self.markdown_table_to_html_professional(
            self.extract_section('Interface Overview', content)
        )
        if interface_table:
            html += f'''
                    <div class="table-section">
                        <h2 class="section-title">COMMUNICATION INTERFACES</h2>
                        {interface_table}
                    </div>
            '''
        
        # COMPONENT REFERENCE TABLE (from hardware README)
        component_table = self.markdown_table_to_html_professional(
            self.extract_section('Component Reference', content)
        )
        if component_table:
            html += f'''
                    <div class="table-section">
                        <h2 class="section-title">COMPONENT REFERENCE</h2>
                        {component_table}
                    </div>
            '''
        
        # MAIN FEATURES
        if features:
            html += '''
                    <div class="features-section">
                        <h2 class="section-title">TECHNICAL FEATURES</h2>
                        <div class="features-grid">
            '''
            for feature in features:
                # Todas las características se muestran directamente como especificaciones técnicas
                # Sin iconos ni títulos genéricos "Feature"
                html += f'''
                        <div class="feature-card">
                            <div class="feature-desc">{str(feature)}</div>
                        </div>
                '''
            html += '''
                        </div>
                    </div>
            '''
        
        # APPLICATIONS
        applications = self.extract_section('Applications', content)
        if applications:
            apps = [line.strip()[2:].strip() for line in applications.split('\n') 
                   if line.strip().startswith('-')]
            if apps:
                html += '''
                        <div class="applications-section">
                            <h2 class="section-title">TYPICAL APPLICATIONS</h2>
                            <div class="applications-grid">
                '''
                for app in apps:
                    if ':' in app:
                        title, desc = app.split(':', 1)
                        html += f'''
                            <div class="app-card">
                                <div class="app-title">{title.strip()}</div>
                                <div>{desc.strip()}</div>
                            </div>
                            '''
                    else:
                        html += f'''
                            <div class="app-card">
                                <div>{app}</div>
                            </div>
                            '''
                html += '''
                            </div>
                        </div>
                '''
        
        # SECCIÓN 1: ESPECIFICACIONES TÉCNICAS Y CARACTERÍSTICAS
        if spec_tables:
            html += '''
                    <div class="tables-section">
                        <h2 class="section-title">TECHNICAL SPECIFICATIONS</h2>
            '''
            for table_info in spec_tables:
                section_title = table_info.get('source_section', 'Specifications').title()
                table_data = table_info.get('data', [])
                if table_data:
                    headers = list(table_data[0].keys()) if table_data else []
                    # OMITIR TABLA DE RECURSOS (Resource/Link) EN ESTA SECCIÓN
                    if any('resource' in h.lower() for h in headers) and any('link' in h.lower() for h in headers):
                        continue
                    markdown_table = f"| {' | '.join(headers)} |\n"
                    markdown_table += f"| {' | '.join(['---'] * len(headers))} |\n"
                    for row in table_data:
                        values = [str(row.get(header, '')) for header in headers]
                        markdown_table += f"| {' | '.join(values)} |\n"
                    table_html = self.markdown_table_to_html_professional(markdown_table, 'technical')
                    html += f'''
                        <div class="table-container">
                            <h3 class="table-title">{section_title}</h3>
                            {table_html}
                        </div>
                    '''
            html += '''
                    </div>
            '''

        # SECCIÓN 2: TYPICAL APPLICATIONS (AHORA DONDE ESTABA ADDITIONAL RESOURCES)
        if app_tables:
            # Buscar la tabla correcta: la que tiene Application/Description vs Resource/Link
            applications_table = None
            for table_info in app_tables:
                table_data = table_info.get('data', [])
                if table_data:
                    headers = list(table_data[0].keys()) if table_data else []
                    # Si contiene "Application" y "Description", es la tabla de aplicaciones  
                    if any('application' in h.lower() for h in headers) and any('description' in h.lower() for h in headers):
                        applications_table = table_info
            # Mostrar solo la tabla de aplicaciones aquí, no la de recursos
            if applications_table:
                html += '''
                        <div class="applications-section">
                            <h2 class="section-title">TYPICAL APPLICATIONS</h2>
                '''
                table_data = applications_table.get('data', [])
                if table_data:
                    headers = list(table_data[0].keys()) if table_data else []
                    markdown_table = f"| {' | '.join(headers)} |\n"
                    markdown_table += f"| {' | '.join(['---'] * len(headers))} |\n"
                    for row in table_data:
                        values = [str(row.get(header, '')) for header in headers]
                        markdown_table += f"| {' | '.join(values)} |\n"
                    table_html = self.markdown_table_to_html_professional(markdown_table, 'applications')
                    html += table_html
                html += '''
                        </div>
                '''

        # All content flows in the same container
        html += '''
        '''
        
        # SECTION 2: DOCUMENTACIÓN VISUAL CON TABLAS CORRESPONDIENTES
        has_images = any([
            images['unit_pinout'],
            images['unit_dimensions'],
            images['unit_top'],
            images['unit_bottom'],
            images['unit_topology'],
            images['unit_schematic']
        ])
        
        if has_images:
            html += '''
                <div class="visual-content">
                    <div class="section-title-major">HARDWARE DOCUMENTATION</div>
            '''
            
            # DIMENSIONES CON ESPECIFICACIONES FÍSICAS
            if images['unit_dimensions']:
                html += f'''
                            <div class="dimensions-section">
                                <div class="section-header">MECHANICAL DIMENSIONS</div>
                                <div class="dimensions-container">
                                    <img src="{images['unit_dimensions']}" alt="Dimensions" class="dimensions-image-large">
                                    <div class="dimensions-caption">Physical dimensions and mounting specifications (measurements in millimeters)</div>
                                </div>
                            </div>
                '''
            
            # TOPOLOGÍA CON TABLA DE COMPONENTES
            if images['unit_topology']:
                html += f'''
                            <div class="topology-section">
                                <div class="section-header">SYSTEM TOPOLOGY</div>
                                <div style="text-align: center;">
                                    <a href="{images['unit_topology']}" target="_blank" class="image-link">
                                        <img src="{images['unit_topology']}" alt="System Topology" class="topology-image-large">
                                    </a>
                                    <div class="doc-caption" style="margin-top: 15px; font-size: 12pt;">
                                        Connection topology and system integration diagram
                                    </div>
                                    <div class="doc-caption" style="font-size: 10pt; color: #6b7280; margin-top: 8px;">
                                        <em>Click image to open in full size</em>
                                    </div>
                                </div>
                '''
                
                # INCLUIR TABLA DE COMPONENTES CON LA TOPOLOGÍA
                if component_tables:
                    html += '''
                                <div class="components-table-section" style="margin-top: 25px;">
                                    <h3 class="table-title">Component Reference</h3>
                    '''
                    for table_info in component_tables:
                        table_data = table_info.get('data', [])
                        if table_data:
                            headers = list(table_data[0].keys()) if table_data else []
                            markdown_table = f"| {' | '.join(headers)} |\n"
                            markdown_table += f"| {' | '.join(['---'] * len(headers))} |\n"
                            
                            for row in table_data:
                                values = [str(row.get(header, '')) for header in headers]
                                markdown_table += f"| {' | '.join(values)} |\n"
                            
                            table_html = self.markdown_table_to_html_professional(markdown_table, 'components')
                            html += table_html
                    html += '''
                                </div>
                    '''
                
                html += '''
                            </div>
                '''
            
            # ESQUEMÁTICO LIMPIO (SIN TABLA DE COMPONENTES - YA ESTÁ EN TOPOLOGÍA)
            if images['unit_schematic']:
                html += f'''
                            <div class="schematic-section">
                                <div class="section-header">CIRCUIT SCHEMATIC</div>
                '''
                
                # Imagen del esquemático
                schematic_pdf = None
                hardware_abs_path = os.path.abspath(self.hardware_path)
                
                if os.path.exists(hardware_abs_path):
                    for file in os.listdir(hardware_abs_path):
                        if 'sch' in file.lower() and file.lower().endswith('.pdf'):
                            schematic_pdf = file
                            break
                
                if not schematic_pdf:
                    hardware_parent_path = os.path.dirname(hardware_abs_path)
                    if os.path.exists(hardware_parent_path):
                        for file in os.listdir(hardware_parent_path):
                            if 'sch' in file.lower() and file.lower().endswith('.pdf'):
                                schematic_pdf = file
                                break
                
                html += f'''
                                <div style="text-align: center; margin-top: 20px;">
                                    <div style="margin-bottom: 20px;">
                                        <img src="{images['unit_schematic']}" alt="Circuit Schematic" class="schematic-image">
                                        <div class="doc-caption" style="margin-top: 10px; font-size: 10pt; color: #6b7280;">
                                            Complete circuit schematic showing all component connections
                                        </div>
                                    </div>
                '''
                if schematic_pdf:
                    html += f'''
                                    <div class="doc-link" style="margin-top: 20px;">
                                        <a href="{schematic_pdf}" target="_blank" class="schematic-link" style="font-size: 14pt; padding: 12px 20px;">
                                            View Complete Schematic PDF
                                        </a>
                                    </div>
                    '''
                
                # AGREGAR ADDITIONAL RESOURCES AQUÍ (SOLO TABLA DE RECURSOS)
                if app_tables:
                    # Buscar solo la tabla de recursos (Resource/Link)
                    for table_info in app_tables:
                        table_data = table_info.get('data', [])
                        if table_data:
                            headers = list(table_data[0].keys()) if table_data else []
                            # Solo procesar si es la tabla de recursos (Resource/Link)
                            if any('resource' in h.lower() for h in headers) and any('link' in h.lower() for h in headers):
                                html += '''
                                    <div class="applications-section" style="margin-top: 30px;">
                                        <h3 style="color: #374151; font-size: 14pt; margin-bottom: 15px; text-align: center;">Additional Resources</h3>
                                '''
                                
                                markdown_table = f"| {' | '.join(headers)} |\n"
                                markdown_table += f"| {' | '.join(['---'] * len(headers))} |\n"
                                
                                for row in table_data:
                                    values = [str(row.get(header, '')) for header in headers]
                                    markdown_table += f"| {' | '.join(values)} |\n"
                                
                                table_html = self.markdown_table_to_html_professional(markdown_table, 'applications')
                                html += table_html
                                html += '''
                                    </div>
                                '''
                                break  # Solo procesar la primera tabla de recursos encontrada
                
                html += '''
                                </div>
                            </div>
                '''
            # ADDITIONAL PRODUCT DETAILS SECTION - DISABLED TO AVOID CLUTTER
            # hardware_path = os.path.abspath(self.hardware_path)
            # additional_images_found = []
            
            # if os.path.exists(hardware_path):
            #     for file in os.listdir(hardware_path):
            #         if file.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            #             file_path = os.path.join(hardware_path, file)
            #             file_lower = file.lower()
            #             
            #             # Skip already displayed main images (flexible naming patterns)
            #             main_image_patterns = ['pinout', 'dimension', 'top', 'btm', 'bottom', 'topology', 'sch', 'schematic', 'circuit']
            #             if any(pattern in file_lower for pattern in main_image_patterns):
            #                 continue
            #             
            #             # Skip obvious non-product images
            #             skip_patterns = ['icon', 'logo', 'watermark', 'template']
            #             if any(pattern in file_lower for pattern in skip_patterns):
            #                 continue
            #             
            #             additional_images_found.append((file, file))
            
            # Only create section if we have additional images
            # if additional_images_found:
            #     html += '''
            #                 <div class="product-details-section">
            #                     <div class="section-header">ADDITIONAL PRODUCT DOCUMENTATION</div>
            #                     <div class="product-details-grid">
            #     '''
            #     
            #     # Display additional images with smart categorization
            #     for file_path, filename in additional_images_found:
            #         file_lower = filename.lower()
            #         
            #         # Smart categorization based on filename patterns (product-agnostic)
            #         if any(x in file_lower for x in ['sch', 'schematic', 'circuit']):
            #             title = "CIRCUIT SCHEMATIC"
            #             description = "Detailed circuit diagram and component layout"
            #         elif any(x in file_lower for x in ['pcb', 'board', 'layout']):
            #             title = "PCB LAYOUT"
            #             description = "Printed circuit board design and routing"
            #         elif any(x in file_lower for x in ['assembly', 'mounting', 'install']):
            #             title = "ASSEMBLY GUIDE"
            #             description = "Installation and mounting instructions"
            #         elif any(x in file_lower for x in ['connection', 'wire', 'cable']):
            #             title = "CONNECTION DIAGRAM"
            #             description = "Wiring and connection examples"
            #         elif any(x in file_lower for x in ['size', 'scale', 'comparison']):
            #             title = "SIZE REFERENCE"
            #             description = "Physical size comparison and scale"
            #         elif any(x in file_lower for x in ['detail', 'close', 'zoom']):
            #             title = "DETAIL VIEW"
            #             description = "Close-up component details"
            #         elif any(x in file_lower for x in ['package', 'box', 'kit']):
            #             title = "PACKAGING"
            #             description = "Product packaging and contents"
            #         else:
            #             # Generic fallback for any other technical image
            #             title = "TECHNICAL REFERENCE"
            #             description = "Additional product documentation"
            #         
            #         # Handle both images and PDFs differently
            #         if filename.lower().endswith('.pdf'):
            #             html += f'''
            #                 <div class="detail-card">
            #                     <div class="detail-title">{title}</div>
            #                     <div class="pdf-placeholder">
            #                         <div class="pdf-icon">📄</div>
            #                         <div class="pdf-text">PDF Document</div>
            #                         <a href="{filename}" target="_blank" class="pdf-link">View {title}</a>
            #                     </div>
            #                     <div class="detail-caption">{description}</div>
            #                 </div>
            #             '''
            #         else:
            #             html += f'''
            #                 <div class="detail-card">
            #                     <div class="detail-title">{title}</div>
            #                     <img src="{filename}" alt="{title}" class="detail-image">
            #                     <div class="detail-caption">{description}</div>
            #                 </div>
            #             '''
            #     
            #     html += '''
            #                     </div>
            #                 </div>
            #     '''
            
            # Close images section
            html += '''
                        </div>
            '''
            
            # Close visual content
            html += '''
                    </div>
            '''
        
        # ADDITIONAL SECTIONS - Usage and Downloads
        usage_section = self.extract_section('Usage', content)
        downloads_section = self.extract_section('Downloads', content)
        
        if usage_section or downloads_section:
            html += '''
                <!-- ADDITIONAL DOCUMENTATION -->
                <div class="additional-sections">
            '''
            
            if usage_section:
                processed_usage = self.process_markdown_content(usage_section)
                html += f'''
                    <div class="section">
                        <h2 class="section-title">Usage</h2>
                        <div class="section-content">
                            {processed_usage}
                        </div>
                    </div>
                '''
            
            if downloads_section:
                processed_downloads = self.process_markdown_content(downloads_section)
                html += f'''
                    <div class="section">
                        <h2 class="section-title">Downloads</h2>
                        <div class="section-content">
                            {processed_downloads}
                        </div>
                    </div>
                '''
            
            html += '''
                </div>
            '''
        
        # PIN DESCRIPTION PAGE - PÁGINA INDEPENDIENTE PARA LA TABLA
        if pinout_tables:
            html += '''
                <!-- PIN DESCRIPTION PAGE - INDEPENDENT PAGE FOR TABLE -->
                <div class="pin-description-page">
                    <div class="pinout-page-title">PIN DESCRIPTION</div>
                    <div class="pinout-page-subtitle">Detailed pin assignment and electrical specifications</div>
                    <div class="components-table-section">
                        <h3 class="table-title">Signal Description</h3>
            '''
            for table_info in pinout_tables:
                table_data = table_info.get('data', [])
                if table_data:
                    headers = list(table_data[0].keys()) if table_data else []
                    markdown_table = f"| {' | '.join(headers)} |\n"
                    markdown_table += f"| {' | '.join(['---'] * len(headers))} |\n"
                    
                    for row in table_data:
                        values = [str(row.get(header, '')) for header in headers]
                        markdown_table += f"| {' | '.join(values)} |\n"
                    
                    table_html = self.markdown_table_to_html_professional(markdown_table, 'components')
                    html += table_html
            html += '''
                    </div>
                </div>
            '''

        # PINOUT LAYOUT PAGE - PÁGINA INDEPENDIENTE PARA LA IMAGEN
        if images['unit_pinout']:
            html += f'''
                <!-- PINOUT LAYOUT PAGE - INDEPENDENT PAGE FOR IMAGE -->
                <div class="pinout-layout-page">
                    <div class="pinout-page-title">PIN CONFIGURATION LAYOUT</div>
                    <div class="pinout-page-subtitle">Physical connector layout and pin positioning</div>
                    <div class="pinout-page-container">
                        <img src="{images['unit_pinout']}" alt="Pin Configuration Layout" class="pinout-page-image">
                    </div>
                    <div class="pinout-page-caption">
                        Complete pin configuration diagram showing all connectors, pin assignments, and electrical connections for proper integration
                    </div>
                </div>
            '''
        
        # Add footer
        html += f'''
                
                <!-- FOOTER -->
                <div class="footer">
                    <div class="footer-grid">
                        <div class="footer-left">
                            <div>© 2025 UNIT Electronics México</div>
                            <div>Technical document automatically generated</div>
                        </div>
                        <div class="footer-center">
                            <div>{product_code} v{version}</div>
                            <div>Professional Technical Datasheet</div>
                        </div>
                        <div class="footer-right">
                            <div>Date: {data['date']}</div>
                            <div>For commercial distribution</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                document.title = '{title}_Professional_Datasheet_v{version}_{data["date"]}';
                
                // Enhanced print function
                function printDatasheet() {{
                    window.print();
                }}
                
                // Configure for printing
                window.addEventListener('beforeprint', () => {{
                    document.body.classList.add('printing');
                }});
                
                window.addEventListener('afterprint', () => {{
                    document.body.classList.remove('printing');
                }});
            </script>
        </body>
        </html>
        '''
        
        # Guardar archivo HTML
        html_path = output_path.replace('.pdf', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Intentar generar PDF usando herramientas disponibles
        pdf_generated = self.convert_html_to_pdf(html_path, output_path)
        
        # Copiar imágenes necesarias al directorio build
        self.copy_images_to_build(images)
        
        # FASE 6: Actualización automática del README principal
        # (Esta funcionalidad se incluirá en una versión futura)
        print(f"Hoja de datos generada: {output_path}")
        print(f"Datos del repositorio descubiertos automáticamente desde: {discovered_data.get('sources', ['README.md'])}")
        print(f"Código del producto detectado: {product_code}")
        
        return {
            'html_path': output_path.replace('.pdf', '.html'),
            'pdf_path': output_path,
            'product_code': product_code,
            'date': date,
            'discovered_sources': discovered_data.get('sources', ['README.md'])
        }

    def extract_electrical_specs_from_discovery(self, discovered_data):
        """Extrae especificaciones eléctricas usando el sistema de descubrimiento mejorado"""
        electrical_specs = []
        connectivity_specs = []
        
        sections = discovered_data.get('sections', {})
        
        # Buscar especificaciones en secciones relevantes
        spec_sections = ['pinout', 'description', 'specifications', 'electrical specifications', 'technical specs', 'connections', 'topology']
        
        for section_name, section_content in sections.items():
            if any(spec in section_name.lower() for spec in spec_sections):
                # Verificar si section_content es un diccionario o una cadena
                if isinstance(section_content, dict):
                    content_text = section_content.get('content', section_content.get('text', ''))
                else:
                    content_text = section_content
                
                if not content_text:
                    continue
                
                # Extraer tablas del contenido
                tables = self.extract_tables_from_text(content_text)
                for table in tables:
                    # Determinar el tipo de tabla
                    if self.is_electrical_spec_table(table):
                        electrical_specs.extend(table)
                    elif self.is_connectivity_table(table) or self.is_pinout_table(table):
                        connectivity_specs.extend(table)
                    elif self.is_component_table(table):
                        # Agregar componentes como especificaciones
                        for row in table:
                            if 'Description' in row and 'Ref.' in row:
                                electrical_specs.append({
                                    'Parameter': f"Component {row['Ref.']}",
                                    'Value': row['Description'],
                                    'Type': 'Component'
                                })
        
        # Si no se encontraron especificaciones, usar valores por defecto basados en BMM150
        if not electrical_specs:
            electrical_specs = [
                {'Parameter': 'Operating Voltage', 'Min': '1.8V', 'Typ': '3.3V', 'Max': '3.6V', 'Unit': 'V'},
                {'Parameter': 'Supply Current', 'Min': '-', 'Typ': '170µA', 'Max': '200µA', 'Unit': 'µA'},
                {'Parameter': 'Operating Temperature', 'Min': '-40°C', 'Typ': '25°C', 'Max': '85°C', 'Unit': '°C'},
                {'Parameter': 'Measurement Range', 'Min': '±1300', 'Typ': '±1300', 'Max': '±1300', 'Unit': 'µT'},
                {'Parameter': 'Resolution', 'Min': '-', 'Typ': '0.3', 'Max': '-', 'Unit': 'µT'},
            ]
        
        if not connectivity_specs:
            connectivity_specs = [
                {'Pin': 'VCC', 'Signal': 'VCC', 'Type': 'Power', 'Description': 'Power supply'},
                {'Pin': 'GND', 'Signal': 'GND', 'Type': 'Ground', 'Description': 'Ground connection'},
                {'Pin': 'SCL', 'Signal': 'SCL', 'Type': 'I/O', 'Description': 'I²C clock'},
                {'Pin': 'SDA', 'Signal': 'SDA', 'Type': 'I/O', 'Description': 'I²C data'},
                {'Pin': 'SDO', 'Signal': 'SDO/ADDR', 'Type': 'I/O', 'Description': 'SPI MISO / I²C address select'},
                {'Pin': 'CS', 'Signal': 'CS', 'Type': 'I/O', 'Description': 'SPI chip-select (active LOW)'},
                {'Pin': 'PS', 'Signal': 'PS', 'Type': 'I/O', 'Description': 'Protocol select (LOW=I²C, HIGH=SPI)'},
                {'Pin': 'DRDY', 'Signal': 'DRDY', 'Type': 'Output', 'Description': 'Data-Ready flag'},
                {'Pin': 'INT', 'Signal': 'INT', 'Type': 'Output', 'Description': 'Programmable interrupt output'},
            ]
        
        return electrical_specs, connectivity_specs

    def is_pinout_table(self, table):
        """Determina si una tabla contiene información de pinout"""
        if not table:
            return False
        
        headers = list(table[0].keys())
        pinout_keywords = ['pin', 'signal', 'description']
        
        return any(keyword in ' '.join(headers).lower() for keyword in pinout_keywords)

    def is_component_table(self, table):
        """Determina si una tabla contiene información de componentes"""
        if not table:
            return False
        
        headers = list(table[0].keys())
        component_keywords = ['ref.', 'ref', 'reference', 'component']
        
        return any(keyword in ' '.join(headers).lower() for keyword in component_keywords)

    def extract_features_from_discovery(self, discovered_data):
        """Extrae características usando el sistema de descubrimiento con mejor procesamiento"""
        features = []
        
        sections = discovered_data.get('sections', {})
        
        # Buscar características específicamente en la sección "Key Features" y similares
        feature_sections = ['key features', 'features', 'functional description', 'characteristics']
        
        for section_name, section_content in sections.items():
            if any(feat in section_name.lower() for feat in feature_sections):
                # Verificar si section_content es un diccionario o una cadena
                if isinstance(section_content, dict):
                    content_text = section_content.get('content', section_content.get('text', ''))
                else:
                    content_text = section_content
                
                if not content_text:
                    continue
                
                # Limpiar el contenido
                clean_content = self.clean_markdown_content(content_text)
                
                # Extraer lista de características
                lines = clean_content.split('\n')
                for line in lines:
                    line = line.strip()
                    
                    # Procesar líneas de lista estándar
                    if line.startswith('- ') or line.startswith('* '):
                        feature = line[2:].strip()
                        if feature and len(feature) > 10:
                            # Limpiar formateo markdown adicional
                            feature = re.sub(r'\*\*([^*]+)\*\*', r'\1', feature)
                            features.append(feature)
                    
                    # Procesar líneas con formato "- **Campo:** Valor"
                    elif line.startswith('- **') and ':' in line:
                        # Extraer tanto el campo como el valor
                        match = re.match(r'- \*\*([^*]+)\*\*:\s*(.+)', line)
                        if match:
                            field_name = match.group(1).strip()
                            field_value = match.group(2).strip()
                            feature = f"{field_name}: {field_value}"
                            features.append(feature)
                    
                    # Procesar líneas con formato "**Campo:** Valor" (sin -)
                    elif line.startswith('**') and ':' in line:
                        match = re.match(r'\*\*([^*]+)\*\*:\s*(.+)', line)
                        if match:
                            field_name = match.group(1).strip()
                            field_value = match.group(2).strip()
                            feature = f"{field_name}: {field_value}"
                            features.append(feature)
        
        # Si no se encontraron características específicas, usar valores por defecto mejorados
        if not features:
            features = [
                "Axes: 3 (X, Y, Z)",
                "Measurement Range: ±1300 µT", 
                "Resolution: ~0.3 µT",
                "Power Consumption: Ultra-low power consumption for battery-operated devices",
                "Interfaces: I²C and SPI",
                "Supply Voltage: 3.3 V",
                "Operating Temperature: Wide operating range suitable for various environments"
            ]
        
        return features
        
        # Si no se encontraron características, usar valores por defecto
        if not features:
            features = [
                "High precision electronic sensor module",
                "Low power consumption design",
                "Wide operating temperature range",
                "Standard interface compatibility",
                "Compact form factor",
                "Professional grade components"
            ]
        
        return features

    def clean_markdown_content(self, content):
        """Limpia contenido markdown removiendo enlaces, imágenes y manteniendo texto"""
        import re
        
        if not content:
            return ""
        
        # Remover bloques de código
        content = re.sub(r'```[\s\S]*?```', '', content)
        content = re.sub(r'`[^`]+`', '', content)
        
        # Remover imágenes markdown
        content = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', content)
        
        # Remover enlaces pero mantener texto
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        
        # Remover enlaces simples
        content = re.sub(r'<[^>]+>', '', content)
        
        # Remover divs y HTML
        content = re.sub(r'<[^>]+>', '', content)
        
        # Remover múltiples asteriscos y negritas
        content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^*]+)\*', r'\1', content)
        
        # Limpiar espacios y líneas extra
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('|'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def extract_applications_from_discovery(self, discovered_data):
        """Extrae aplicaciones usando el sistema de descubrimiento"""
        applications = []
        
        sections = discovered_data.get('sections', {})
        
        # Buscar aplicaciones en secciones relevantes
        app_sections = ['applications', 'use cases', 'examples', 'usage']
        
        for section_name, section_content in sections.items():
            if any(app in section_name.lower() for app in app_sections):
                # Verificar si section_content es un diccionario o una cadena
                if isinstance(section_content, dict):
                    content_text = section_content.get('content', section_content.get('text', ''))
                else:
                    content_text = section_content
                
                if not content_text:
                    continue
                
                lines = content_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('- ') or line.startswith('* '):
                        app = line[2:].strip()
                        if app and len(app) > 5:
                            applications.append(app)
        
        # Si no se encontraron aplicaciones, usar valores por defecto
        if not applications:
            applications = [
                "Industrial automation systems",
                "IoT sensor networks",
                "Environmental monitoring",
                "Research and development projects",
                "Educational electronics platforms",
                "Prototype development"
            ]
        
        return applications

    def convert_html_to_pdf(self, html_path, pdf_path):
        """Convierte HTML a PDF usando herramientas disponibles en el sistema"""
        import subprocess
        import shutil
        
        # Lista de herramientas para conversión HTML a PDF (en orden de preferencia)
        tools = [
            {
                'command': 'wkhtmltopdf',
                'args': ['--page-size', 'A4', '--orientation', 'Portrait', 
                        '--margin-top', '20mm', '--margin-bottom', '20mm',
                        '--margin-left', '15mm', '--margin-right', '15mm',
                        '--print-media-type', '--enable-local-file-access']
            },
            {
                'command': 'weasyprint',
                'args': []
            },
            {
                'command': 'chromium-browser',
                'args': ['--headless', '--disable-gpu', '--print-to-pdf-no-header', 
                        '--print-to-pdf']
            },
            {
                'command': 'google-chrome',
                'args': ['--headless', '--disable-gpu', '--print-to-pdf-no-header', 
                        '--print-to-pdf']
            }
        ]
        
        for tool in tools:
            if shutil.which(tool['command']):
                try:
                    cmd = [tool['command']] + tool['args'] + [html_path, pdf_path]
                    
                    # Ajuste especial para Chrome/Chromium
                    if 'chrome' in tool['command'] or 'chromium' in tool['command']:
                        cmd = [tool['command']] + tool['args'] + [f'--print-to-pdf={pdf_path}', f'file://{html_path}']
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0 and os.path.exists(pdf_path):
                        print(f"✅ PDF generado exitosamente usando {tool['command']}")
                        return True
                    else:
                        print(f"⚠️ Error con {tool['command']}: {result.stderr}")
                        
                except Exception as e:
                    print(f"⚠️ Error ejecutando {tool['command']}: {e}")
                    continue
        
        # Si no se pudo generar PDF, crear una copia del HTML con extensión .pdf
        print("⚠️ No se encontraron herramientas para conversión PDF. Creando marcador HTML.")
        shutil.copy2(html_path, pdf_path)
        print("💡 Para generar PDF real, instala: sudo apt install wkhtmltopdf")
        return False

    def convert_specs_list_to_dict(self, specs_list):
        """Convierte lista de especificaciones a diccionario para compatibilidad"""
        specs_dict = {}
        
        if not specs_list:
            return specs_dict
        
        for spec in specs_list:
            if isinstance(spec, dict):
                # Buscar una clave que represente el parámetro/nombre
                param_key = spec.get('Parameter', spec.get('Name', spec.get('Pin', '')))
                if param_key:
                    # Buscar valor en diferentes campos posibles
                    value = spec.get('Typ', spec.get('Value', spec.get('Description', spec.get('Type', ''))))
                    if value:
                        specs_dict[param_key] = value
        
        return specs_dict

    def extract_tables_from_text(self, text):
        """Extrae tablas de formato markdown de un texto con mejor detección"""
        tables = []
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Buscar líneas que parecen cabecera de tabla (deben tener al menos 2 |)
            if line.count('|') >= 2 and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                
                # Verificar si la siguiente línea es separador de tabla
                if next_line.count('|') >= 2 and ('-' in next_line or ':' in next_line):
                    # Extraer cabeceras
                    headers = [cell.strip() for cell in line.split('|') if cell.strip()]
                    
                    # Si no hay cabeceras válidas, continuar
                    if not headers:
                        i += 1
                        continue
                    
                    table_data = []
                    j = i + 2  # Saltar línea de cabecera y separador
                    
                    # Extraer filas de datos
                    while j < len(lines):
                        row_line = lines[j].strip()
                        
                        # Si la línea tiene suficientes | y no está vacía
                        if row_line.count('|') >= 2 and row_line:
                            # Limpiar enlaces markdown de la fila (se procesarán después según el tipo)
                            row_line_clean = row_line
                            row_data = [cell.strip() for cell in row_line_clean.split('|') if cell.strip()]
                            
                            # Solo agregar si tiene datos válidos
                            if len(row_data) >= len(headers):
                                row_dict = {}
                                for k, header in enumerate(headers):
                                    if k < len(row_data):
                                        row_dict[header] = row_data[k]
                                table_data.append(row_dict)
                            j += 1
                        else:
                            break
                    
                    # Solo agregar la tabla si tiene datos
                    if table_data:
                        tables.append(table_data)
                    i = j
                else:
                    i += 1
            else:
                i += 1
        
        return tables

    def convert_markdown_links_to_html(self, text):
        """Convierte enlaces markdown a HTML"""
        import re
        
        # Patrón para enlaces markdown [texto](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        # Reemplazar con enlaces HTML
        html_links = re.sub(link_pattern, r'<a href="\2" target="_blank">\1</a>', text)
        
        return html_links

    def clean_markdown_links(self, text):
        """Limpia enlaces markdown pero mantiene el texto"""
        import re
        
        # Patrón para enlaces markdown [texto](url)
        link_pattern = r'\[([^\]]+)\]\([^)]+\)'
        # Reemplazar con solo el texto
        cleaned = re.sub(link_pattern, r'\1', text)
        
        # Patrón para enlaces simples <url>
        simple_link_pattern = r'<[^>]+>'
        cleaned = re.sub(simple_link_pattern, '', cleaned)
        
        # Limpiar espacios extra
        cleaned = ' '.join(cleaned.split())
        
        return cleaned

    def is_electrical_spec_table(self, table):
        """Determina si una tabla contiene especificaciones eléctricas"""
        if not table:
            return False
        
        headers = list(table[0].keys())
        electrical_keywords = ['voltage', 'current', 'power', 'temperature', 'parameter', 'min', 'max', 'typ']
        
        return any(keyword in ' '.join(headers).lower() for keyword in electrical_keywords)

    def is_connectivity_table(self, table):
        """Determina si una tabla contiene información de conectividad"""
        if not table:
            return False
        
        headers = list(table[0].keys())
        connectivity_keywords = ['pin', 'connector', 'signal', 'name', 'type', 'description']
        
        return any(keyword in ' '.join(headers).lower() for keyword in connectivity_keywords)
        """Procesa contenido markdown básico: enlaces y listas"""
        if not content:
            return ""
        
        import re
        
        # Eliminar emojis de caracteres unicode
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        content = emoji_pattern.sub('', content)
        
        # Procesar enlaces markdown [texto](url)
        def replace_link(match):
            text = match.group(1)
            url = match.group(2)
            return f'<a href="{url}" target="_blank" style="color: #374151; text-decoration: underline;">{text}</a>'
        
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
        
        # Procesar listas con guiones
        lines = content.split('\n')
        processed_lines = []
        in_list = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                if not in_list:
                    processed_lines.append('<ul style="margin: 10px 0; padding-left: 20px;">')
                    in_list = True
                item_content = line[2:].strip()
                processed_lines.append(f'<li style="color: #374151; font-size: 11pt;">{item_content}</li>')
            else:
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                processed_lines.append(f'<p style="margin: 10px 0; color: #374151;">{line}</p>')
        
        if in_list:
            processed_lines.append('</ul>')
        
        return '\n'.join(processed_lines)

    def extract_introduction(self, content):
        """Extrae párrafos de introducción desde el contenido principal"""
        paragraphs = []
        
        # Extraer el primer párrafo del documento (generalmente la descripción principal)
        lines = content.split('\n')
        first_paragraph = ""
        
        for line in lines:
            line = line.strip()
            # Saltar encabezados, imágenes y enlaces
            if (line.startswith('#') or 
                line.startswith('<div') or 
                line.startswith('![') or 
                line.startswith('<a') or
                line.startswith('|') or
                line == ''):
                continue
            
            # Si encontramos texto real, es probablemente la introducción
            if line and not line.startswith('-') and not line.startswith('*'):
                first_paragraph = line
                break
        
        if first_paragraph:
            # Limpiar markdown
            clean_para = first_paragraph.replace('**', '').replace('*', '')
            paragraphs.append(clean_para)
        
        # Si no se encontró introducción, usar una genérica basada en el título
        if not paragraphs:
            paragraphs = [
                "Professional electronic module designed for reliable performance and easy integration.",
                "Features modern communication interfaces and robust design for various applications."
            ]
        
        return paragraphs

    def update_main_readme(self, main_readme_path, hardware_data):
        """Actualiza el README principal con información complementaria del hardware"""
        if not hardware_data:
            print("⚠️ No hardware data available for README update")
            return
        
        # Leer README principal actual
        with open(main_readme_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        hardware_content = hardware_data['content']
        
        # Extraer información útil del hardware
        pinout_table = self.extract_pinout_table(hardware_content)
        component_table = self.extract_component_table(hardware_content)
        
        updated_content = main_content
        
        # Agregar sección de pinout si no existe
        if pinout_table and '## Pinout' not in main_content and '## Pin Configuration' not in main_content:
            # Buscar donde insertar la sección de pinout (después de Features)
            lines = updated_content.split('\n')
            insert_index = -1
            
            for i, line in enumerate(lines):
                if line.strip().startswith('## Applications'):
                    insert_index = i
                    break
            
            if insert_index > 0:
                pinout_section = f"""
## Pinout

{pinout_table}

"""
                lines.insert(insert_index, pinout_section)
                updated_content = '\n'.join(lines)
                print("✅ Added pinout section to main README")
        
        # Agregar sección de componentes si no existe
        if component_table and '## Component Reference' not in main_content:
            # Agregar al final antes de Documentation
            lines = updated_content.split('\n')
            insert_index = -1
            
            for i, line in enumerate(lines):
                if line.strip().startswith('## Documentation'):
                    insert_index = i
                    break
            
            if insert_index > 0:
                component_section = f"""
## Component Reference

{component_table}

"""
                lines.insert(insert_index, component_section)
                updated_content = '\n'.join(lines)
                print("✅ Added component reference section to main README")
        
        # Guardar README actualizado
        if updated_content != main_content:
            backup_path = main_readme_path + '.backup'
            shutil.copy2(main_readme_path, backup_path)
            print(f"📋 Backup created: {backup_path}")
            
            with open(main_readme_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✅ Main README updated: {main_readme_path}")
        else:
            print("ℹ️ No updates needed for main README")


def main():
    """Función principal para probar el generador con sistema de descubrimiento automático"""
    import os
    
    # Detectar automáticamente el directorio del repositorio
    current_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    print(f"🔍 Iniciando generador con descubrimiento automático")
    print(f"📁 Directorio del repositorio: {repo_root}")
    
    # Crear generador
    generator = ProfessionalDatasheetGenerator(current_dir)
    
    # Generar hoja de datos usando descubrimiento automático
    readme_path = os.path.join(repo_root, 'README.md')
    output_path = os.path.join(current_dir, 'build', 'datasheet_professional.pdf')
    
    try:
        result = generator.generate_professional_datasheet(readme_path, output_path)
        print(f"\n✅ Generación completada exitosamente!")
        print(f"📄 PDF: {result['pdf_path']}")
        print(f"🌐 HTML: {result['html_path']}")
        print(f"🏷️  Código del producto: {result['product_code']}")
        print(f"📅 Fecha: {result['date']}")
        print(f"📚 Fuentes descubiertas: {', '.join(result['discovered_sources'])}")
        
    except Exception as e:
        print(f"❌ Error durante la generación: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
