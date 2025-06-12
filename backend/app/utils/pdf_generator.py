from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from typing import List, Dict, Any

def generate_shopping_list_pdf(shopping_list: Any, market_comparisons: List[Dict[str, Any]]) -> bytes:
    """
    Alışveriş listesini PDF formatında oluştur.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Başlık
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    elements.append(Paragraph(shopping_list.name, title_style))
    elements.append(Spacer(1, 20))

    # Ürün Listesi
    elements.append(Paragraph("Ürün Listesi", styles['Heading2']))
    elements.append(Spacer(1, 10))

    # Ürün tablosu
    product_data = [['Ürün', 'Adet', 'Birim Fiyat', 'Toplam']]
    for item in shopping_list.items:
        product_data.append([
            item.product.name,
            str(item.quantity),
            f"{item.product.details[0].price:.2f} TL",
            f"{(item.product.details[0].price * item.quantity):.2f} TL"
        ])

    product_table = Table(product_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(product_table)
    elements.append(Spacer(1, 30))

    # Market Karşılaştırması
    elements.append(Paragraph("Market Karşılaştırması", styles['Heading2']))
    elements.append(Spacer(1, 10))

    # Market karşılaştırma tablosu
    market_data = [['Market', 'Toplam Fiyat', 'Tasarruf']]
    base_price = market_comparisons[0]['total_price'] if market_comparisons else 0
    
    for comparison in market_comparisons:
        savings = base_price - comparison['total_price']
        market_data.append([
            comparison['market_name'],
            f"{comparison['total_price']:.2f} TL",
            f"{savings:.2f} TL"
        ])

    market_table = Table(market_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(market_table)
    elements.append(Spacer(1, 30))

    # Her market için detaylı ürün listesi
    for comparison in market_comparisons:
        elements.append(Paragraph(f"{comparison['market_name']} - Ürün Listesi", styles['Heading3']))
        elements.append(Spacer(1, 10))

        market_items_data = [['Ürün', 'Adet', 'Birim Fiyat', 'Toplam']]
        for item in comparison['items']:
            market_items_data.append([
                item['product_name'],
                str(item['quantity']),
                f"{item['price']:.2f} TL",
                f"{(item['price'] * item['quantity']):.2f} TL"
            ])

        market_items_table = Table(market_items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        market_items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(market_items_table)
        elements.append(Spacer(1, 20))

    # PDF oluştur
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf 