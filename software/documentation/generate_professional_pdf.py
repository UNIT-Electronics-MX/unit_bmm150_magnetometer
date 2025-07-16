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
import shutil
from datetime import datetime
from zoneinfo import ZoneInfo


class ProfessionalDatasheetGenerator:
    def __init__(self):
        self.css_professional = self.get_professional_css()
        self.hardware_path = "../../hardware/resources"
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
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
        
        /* ADDITIONAL SECTIONS (USAGE, DOWNLOADS) - Force page break */
        .additional-sections {
            page-break-before: always !important;
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
            background: #6b7280 !important;
            color: white !important;
            font-weight: bold;
            text-align: center;
            font-size: 10pt;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
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
            
            /* ADDITIONAL SECTIONS (USAGE, DOWNLOADS) - Nueva página */
            .additional-sections {
                page-break-before: always;
                page-break-inside: avoid;
                margin: 5mm 0;
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
                max-width: 80mm;
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
            max-width: 450px;
            height: auto;
            object-fit: contain;
            border-radius: 6px;
            background: white;
            padding: 8px;
            display: block;
            margin: 0 auto;
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
            page-break-after: always;
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
                height: 297mm !important;
                margin: 0 !important;
                padding: 8mm !important;
                page-break-before: always !important;
                page-break-after: always !important;
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
            padding: 8px 15px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 9pt;
            font-weight: 500;
            transition: all 0.3s ease;
            border: 2px solid #374151;
        }
        
        .schematic-link:hover {
            background: white;
            color: #374151;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
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
                elif any(pattern in file_lower for pattern in ['sch', 'schematic', 'circuit']) and '.pdf' not in file_lower:
                    images['unit_schematic'] = file
        
        
        return images

    def extract_electrical_specs(self, content):
        """Extrae especificaciones eléctricas detalladas"""
        electrical_section = self.extract_section('Electrical Characteristics & Signal Overview', content)
        
        specs = {}
        connectivity = {}
        
        if electrical_section:
            lines = electrical_section.split('\n')
            for line in lines:
                line = line.strip()
                if ':' in line and line.startswith('-'):
                    # Formato "- Especificación: valor"
                    clean_line = line[1:].strip()  # Quitar el guión
                    if ':' in clean_line:
                        key, value = clean_line.split(':', 1)
                        key_clean = key.strip()
                        value_clean = value.strip()
                        
                        # Detectar información de conectividad
                        if 'interface' in key_clean.lower() or 'communication' in key_clean.lower():
                            connectivity['interfaces'] = value_clean
                        elif 'connector' in key_clean.lower():
                            connectivity['connector'] = value_clean
                        else:
                            specs[key_clean] = value_clean
                            
                elif 'power supply' in line.lower():
                    match = re.search(r'([0-9.]+V?\s*to\s*[0-9.]+V?)', line, re.IGNORECASE)
                    if match:
                        specs['Power supply'] = match.group(1)
                elif 'consumption' in line.lower() or 'current' in line.lower():
                    specs['Low power consumption'] = line.split(':', 1)[-1].strip() if ':' in line else line.strip('- ')
        
        return specs, connectivity

    def extract_features_detailed(self, content):
        """Extrae características con más detalle"""
        features_section = self.extract_section('Features', content)
        features = []
        
        if features_section:
            lines = features_section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- '):
                    feature = line[2:].strip()
                    # Eliminar emojis de la línea de característica
                    feature = self.process_markdown_content(feature).replace('<p style="margin: 10px 0; color: #374151;">', '').replace('</p>', '')
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
        
        html = f'<table class="{table_class}">\n<thead>\n<tr>\n'
        for header in headers:
            html += f'<th>{header}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        
        for i, row in enumerate(rows):
            html += '<tr>\n'
            for j, cell in enumerate(row):
                if table_type == 'pinout':
                    if j == 0 and (cell.isdigit() or 'pin' in cell.lower()):
                        html += f'<td><div class="pin-number">{cell}</div></td>\n'
                    elif j == 1 or 'pin' in headers[j].lower():
                        html += f'<td class="pin-name">{cell}</td>\n'
                    else:
                        html += f'<td class="pin-function">{cell}</td>\n'
                else:
                    html += f'<td>{cell}</td>\n'
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
        
        # Copiar PDFs de esquemáticos
        if os.path.exists(hardware_abs_path):
            for file in os.listdir(hardware_abs_path):
                if 'sch' in file.lower() and file.lower().endswith('.pdf'):
                    source_path = os.path.join(hardware_abs_path, file)
                    dest_path = os.path.join(build_dir, file)
                    shutil.copy2(source_path, dest_path)
                    print(f"📋 Copied schematic PDF {file} to build/")

    def generate_professional_datasheet(self, readme_path, output_path):
        """Genera hoja de datos profesional completa"""
        # Parsear README
        data = self.parse_readme(readme_path)
        frontmatter = data['frontmatter']
        content = data['content']
        
        # Extraer información (valores por defecto genéricos)
        title = frontmatter.get('title', 'Electronic Module')
        subtitle = frontmatter.get('subtitle', 'Professional sensor module')
        version = frontmatter.get('version', '1.0')
        
        # Extraer código del producto de forma genérica
        # Buscar patrones comunes: UE+números, BME+números, o palabras en mayúsculas
        product_code_match = re.search(r'(UE\d+|BME\d+|[A-Z]{2,}\d+|\b[A-Z]{3,}\b)', title.upper())
        if product_code_match:
            product_code = product_code_match.group(1)
        else:
            # Si no se encuentra un patrón, usar las primeras palabras del título
            words = title.upper().split()
            if len(words) >= 2:
                product_code = ''.join(word[:3] for word in words[:2] if word.isalpha())
            else:
                product_code = "MODULE"
        
        # Obtener imágenes de hardware
        images = self.find_hardware_images()
        electrical_specs, connectivity_specs = self.extract_electrical_specs(content)
        features = self.extract_features_detailed(content)
        key_features = self.extract_key_features(content)
        introduction_paragraphs = self.extract_introduction(content)
        
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
            <a href="#" class="download-button no-print" onclick="window.print()">
                Download PDF
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
        if electrical_specs:
            html += '''
                <div class="key-specs">
                    <div class="specs-title">KEY TECHNICAL<br>SPECIFICATIONS</div>
                    <div class="specs-grid">
            '''
            
            # Group specifications
            power_specs = {}
            
            for key, value in electrical_specs.items():
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
            interfaces = connectivity_specs.get('interfaces', 'I²C, SPI')
            connector = connectivity_specs.get('connector', 'Qwiic + Pin Headers')
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
        
        # MAIN FEATURES
        if features:
            html += '''
                    <div class="features-section">
                        <h2 class="section-title">TECHNICAL FEATURES</h2>
                        <div class="features-grid">
            '''
            for feature in features:
                html += f'''
                        <div class="feature-card">
                            <div class="feature-title">{feature['icon']} {feature['title']}</div>
                            <div class="feature-desc">{feature['desc']}</div>
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
        
        # All content flows in the same container
        html += '''
        '''
        
        # SECTION 2: ALL VISUAL CONTENT AT THE END - Only if we have images
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
                    <div class="section-title-major">VISUAL DOCUMENTATION</div>
            '''
            
            # MAIN TECHNICAL IMAGES (LARGE FORMAT FOR A4) - WITHOUT PINOUT
            html += '''
                    <div class="images-section">
                        <div class="images-title">PRIMARY TECHNICAL DOCUMENTATION</div>
            '''
            
            # Dimensions - LARGE
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
            # Additional Technical Documentation - Only if available
            additional_images = []
            if images['unit_topology']:
                additional_images.append(('unit_topology', 'System Topology', 'Connection topology and system integration'))
            if images['unit_schematic']:
                additional_images.append(('unit_schematic', 'Circuit Schematic', 'Detailed circuit schematic diagram'))
                
            if additional_images:
                html += '''
                            <div class="additional-docs-section">
                                <div class="section-header">SUPPLEMENTARY TECHNICAL DOCUMENTATION</div>
                                <div class="additional-docs-grid">
                '''
                
                for img_key, title, description in additional_images:
                    # Special handling for schematic with PDF link
                    if img_key == 'unit_schematic':
                        # Find schematic PDF file
                        schematic_pdf = None
                        hardware_abs_path = os.path.abspath(self.hardware_path)
                        if os.path.exists(hardware_abs_path):
                            for file in os.listdir(hardware_abs_path):
                                if 'sch' in file.lower() and file.lower().endswith('.pdf'):
                                    schematic_pdf = file  # Solo usar el nombre del archivo
                                    break
                        
                        html += f'''
                                    <div class="doc-card">
                                        <div class="doc-title">{title.upper()}</div>
                                        <img src="{images[img_key]}" alt="{title}" class="topology-image">
                                        <div class="doc-caption">{description}</div>
                        '''
                        if schematic_pdf:
                            html += f'''
                                        <div class="doc-link">
                                            <a href="{schematic_pdf}" target="_blank" class="schematic-link">
                                                📄 View Complete Schematic PDF
                                            </a>
                                        </div>
                            '''
                        html += '''
                                    </div>
                        '''
                    else:
                        html += f'''
                                    <div class="doc-card">
                                        <div class="doc-title">{title.upper()}</div>
                                        <img src="{images[img_key]}" alt="{title}" class="topology-image">
                                        <div class="doc-caption">{description}</div>
                                    </div>
                        '''
                
                html += '''
                                </div>
                            </div>
                '''
            # ADDITIONAL PRODUCT DETAILS SECTION - Only include if there are additional images
            hardware_path = os.path.abspath(self.hardware_path)
            additional_images_found = []
            
            if os.path.exists(hardware_path):
                for file in os.listdir(hardware_path):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file_path = os.path.join(hardware_path, file)
                        file_lower = file.lower()
                        
                        # Skip already displayed main images (flexible naming patterns)
                        main_image_patterns = ['pinout', 'dimension', 'top', 'btm', 'bottom', 'topology']
                        if any(pattern in file_lower for pattern in main_image_patterns):
                            continue
                        
                        # Skip obvious non-product images
                        skip_patterns = ['icon', 'logo', 'watermark', 'template']
                        if any(pattern in file_lower for pattern in skip_patterns):
                            continue
                        
                        additional_images_found.append((file_path, file))
            
            # Only create section if we have additional images
            if additional_images_found:
                html += '''
                            <div class="product-details-section">
                                <div class="section-header">ADDITIONAL PRODUCT DOCUMENTATION</div>
                                <div class="product-details-grid">
                '''
                
                # Display additional images with smart categorization
                for file_path, filename in additional_images_found:
                    file_lower = filename.lower()
                    
                    # Smart categorization based on filename patterns (product-agnostic)
                    if any(x in file_lower for x in ['sch', 'schematic', 'circuit']):
                        title = "CIRCUIT SCHEMATIC"
                        description = "Detailed circuit diagram and component layout"
                    elif any(x in file_lower for x in ['pcb', 'board', 'layout']):
                        title = "PCB LAYOUT"
                        description = "Printed circuit board design and routing"
                    elif any(x in file_lower for x in ['assembly', 'mounting', 'install']):
                        title = "ASSEMBLY GUIDE"
                        description = "Installation and mounting instructions"
                    elif any(x in file_lower for x in ['connection', 'wire', 'cable']):
                        title = "CONNECTION DIAGRAM"
                        description = "Wiring and connection examples"
                    elif any(x in file_lower for x in ['size', 'scale', 'comparison']):
                        title = "SIZE REFERENCE"
                        description = "Physical size comparison and scale"
                    elif any(x in file_lower for x in ['detail', 'close', 'zoom']):
                        title = "DETAIL VIEW"
                        description = "Close-up component details"
                    elif any(x in file_lower for x in ['package', 'box', 'kit']):
                        title = "PACKAGING"
                        description = "Product packaging and contents"
                    else:
                        # Generic fallback for any other technical image
                        title = "TECHNICAL REFERENCE"
                        description = "Additional product documentation"
                    
                    html += f'''
                        <div class="detail-card">
                            <div class="detail-title">{title}</div>
                            <img src="{file_path}" alt="{title}" class="detail-image">
                            <div class="detail-caption">{description}</div>
                        </div>
                    '''
                
                html += '''
                                </div>
                            </div>
                '''
            
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
        
        # PINOUT PAGE - INDEPENDENT AT THE END
        if images['unit_pinout']:
            html += f'''
                <!-- PINOUT PAGE - INDEPENDENT SECTION -->
                <div class="pinout-page">
                    <div class="pinout-page-title">PIN CONFIGURATION & LAYOUT</div>
                    <div class="pinout-page-subtitle">Detailed pin assignment and connector layout</div>
                    <div class="pinout-page-container">
                        <img src="{images['unit_pinout']}" alt="Pin Configuration" class="pinout-page-image">
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
        
        # Guardar archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Copiar imágenes necesarias al directorio build
        self.copy_images_to_build(images)
        
        return output_path

    def process_markdown_content(self, content):
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
        """Extrae párrafos de la sección Introduction"""
        introduction_section = self.extract_section('Introduction', content)
        paragraphs = []
        
        if introduction_section:
            # Procesar el contenido markdown para eliminar emojis y convertir enlaces
            processed_content = self.process_markdown_content(introduction_section)
            
            # Dividir en párrafos (por líneas en blanco dobles o saltos simples)
            raw_paragraphs = [p.strip() for p in introduction_section.split('\n\n') if p.strip()]
            
            for para in raw_paragraphs:
                # Limpiar y procesar cada párrafo
                clean_para = self.process_markdown_content(para)
                if clean_para:
                    paragraphs.append(clean_para)
        
        return paragraphs


if __name__ == "__main__":
    import subprocess
    import shutil
    
    generator = ProfessionalDatasheetGenerator()
    
    # Paths
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    output_path = os.path.join(os.path.dirname(__file__), 'build', 'datasheet_professional.html')
    pdf_path = os.path.join(os.path.dirname(__file__), 'build', 'datasheet_professional.pdf')
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate datasheet
    try:
        result_path = generator.generate_professional_datasheet(readme_path, output_path)
        print(f"✅ Professional datasheet HTML generated: {result_path}")
        
        # Generate PDF using Chrome/Chromium
        chrome_browsers = [
            'google-chrome',
            'google-chrome-stable', 
            'chromium-browser',
            'chromium'
        ]
        
        chrome_cmd = None
        for browser in chrome_browsers:
            if shutil.which(browser):
                chrome_cmd = browser
                break
        
        if chrome_cmd:
            try:
                subprocess.run([
                    chrome_cmd,
                    '--headless',
                    '--disable-gpu',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--print-to-pdf=' + pdf_path,
                    result_path
                ], check=True, capture_output=True)
                print(f"✅ Professional datasheet PDF generated: {pdf_path}")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ PDF generation failed: {e}")
                print("HTML file is still available")
        else:
            print("⚠️ No Chrome/Chromium browser found. PDF not generated.")
            print("HTML file is available")
            
    except Exception as e:
        print(f"❌ Error generating datasheet: {e}")
        import traceback
        traceback.print_exc()
