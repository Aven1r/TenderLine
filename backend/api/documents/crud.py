from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas
from ..auth.schemas import User
from .schemas import UserContractInfo
from .models import Document
import os
from reportlab.platypus import PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, TA_CENTER, TA_JUSTIFY, TA_RIGHT


async def get_document(session: AsyncSession, _id: int):
    rez = await session.execute(select(Document).where(Document.id == _id))
    return rez.scalar_one_or_none()

async def create_document(session: AsyncSession, document: schemas.DocumentCreate) -> Document:
    document_db = Document(**document.model_dump())
    session.add(document_db)
    await session.commit()
    await session.refresh(document_db)
    return document_db


translations = {
    "status": "Cтатус",
    "reestr_number": "Реестровый номер",
    "purchase_number": "Осуществленная закупка",
    "law_number": "Закон заключения контракта",
    "contract_method": "Способ размещения",
    "contract_basis": "Основание заключения",
    "contract_number": "Номер контракта",
    "contract_lifetime": "Срок действия",
    "contract_subject": "Предмет контракта",
    "contract_place": "Место поставки",
    "IKZ": "ИКЗ",
    "budget": "Источник финансирования",
    "contract_price": "Цена контракта",
    "prepayment": "Аванс",
}

async def get_difference(document1: schemas.Document, document2: schemas.Document):
    diffs = {}

    for key in document1.__dict__.keys():
        if document1.__dict__[key] != document2.__dict__[key]:
            russian_key = translations[key]
            diffs[russian_key] = (document1.__dict__[key], document2.__dict__[key])

    return diffs


async def generate_pdf(document: schemas.Document, user1: UserContractInfo, user2: UserContractInfo):
    pdfmetrics.registerFont(TTFont('TMR', os.path.abspath("backend/api/documents/fonts/TimesNewRoman.ttf")))
    pdfmetrics.registerFont(TTFont('TMRB', os.path.abspath("backend/api/documents/fonts/TimesNewRomanBold.ttf")))

    style = ParagraphStyle('russian_text', fontName='TMR', leading=0.5 * cm, alignment=TA_JUSTIFY, fontSize=10)
    left_allign = ParagraphStyle('russian_text', fontName='TMR', leading=0.5 * cm, fontSize=10)
    style_bold = ParagraphStyle('russian_text', fontName='TMRB', leading=0.5 * cm, alignment=TA_CENTER, fontSize=10)
    left_allign_bold = ParagraphStyle('russian_text', fontName='TMRB', leading=0.5 * cm, fontSize=10)
    right_allign = ParagraphStyle('russian_text', fontName='TMR', leading=0.5 * cm, alignment=TA_RIGHT, fontSize=10)

    doc = SimpleDocTemplate('backend/api/documents/generated/hackcontract.pdf', pagesize=letter)
    story = []

    story.append(Paragraph("Договор №2024", style_bold))
    story.append(Paragraph("На поставку Елочных игрушек", style_bold))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("г. Пермь", left_allign))
    story.append(Paragraph("<br/>\n<br/>", style))

    text = f"""{user1.company_name}, 
    в лице директора Агафонова Валерия Алексеевича, действующего на основании Устава, 
    именуемый в дальнейшем «Поставщик» и {user2.company_name}, в лице главного врача Михайленко Дениса Валерьевича, действующего на основании Устава, именуемый в дальнейшем «Заказчик», в соответствии с требованиями 
    {document.contract_basis} Федерального закона от 05 апреля 2013 года {document.law_number} «О контрактной системе в сфере закупок товаров, работ, услуг для обеспечения государственных и муниципальных нужд», заключили настоящий Договор о нижеследующем:
    """
    story.append(Paragraph(text, style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("1. ПРЕДМЕТ ДОГОВОРА", style_bold))
    story.append(Paragraph(
        f"""1.1. Поставщик обязуется поставить, а Заказчик обязуется оплатить в обусловленный срок – Товар в соответствии с условиями договора и Спецификацией к нему (Приложение №2).""",
        style))
    story.append(Paragraph(f"1.2. ИКЗ: {document.IKZ}", style))
    story.append(Paragraph(f"1.3. Источник финансирования:{document.budget}", style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("2. ЦЕНА И ПОРЯДОК РАСЧЕТОВ", style_bold))
    story.append(
        Paragraph(f"2.1. Цена настоящего договора {document.contract_price} рублей, 00 коп. без налога (НДС).", style))
    text = """2.2. Цена Договора является твердой и определяется на весь срок исполнения Договора, за исключением случаев, установленных в Законе о контрактной системе<br/>
        2.3. Цена договора включает в себя стоимость Товара, расходы на выполнение Спецификации (Приложение №1) в полном объеме, перевозку.<br/>
        2.4 Оплата за поставленный товар осуществляется заказчиком безналичным перечислением денежных средств в течение 10 (десяти) рабочих дней после проведения Заказчиком приемки товара и предоставления Поставщиком надлежащим образом оформленных платежных документов: счета, счет-фактуры и товарной накладной.<br/>"""
    story.append(Paragraph(text, style))
    if document.prepayment != None:
        story.append(Paragraph(f"2.5. Аванс составляет {document.prepayment} рублей, 00 коп. без налога (НДС).", style))
    else:
        story.append(Paragraph("2.5. Аванс не предусмотрен", style))
    text = """2.6. Сумма по Договору, подлежащая уплате Поставщику, уменьшается на размер налогов, сборов и иных обязательных платежей в бюджеты бюджетной системы Российской Федерации, связанных с оплатой Договора, если в соответствии с законодательством Российской Федерации о налогах и сборах такие налоги, сборы и иные обязательные платежи подлежат уплате в бюджеты бюджетной системы Российской Федерации Заказчиком.<br/>
            2.7. Цена Договора может быть изменена, если по предложению Заказчика увеличивается или уменьшается предусмотренное Договором количество Товара не более чем на десять процентов.<br/>
            При этом по соглашению Сторон допускается изменение с учетом положений бюджетного законодательства Российской Федерации цены Договора пропорционально дополнительному количеству Товара исходя из установленной в Договоре цены единицы Товара, но не более чем на десять процентов цены Договора. При уменьшении предусмотренного Договором количества Товара Стороны Договора обязаны уменьшить цену Договора исходя из цены единицы Товара.<br/>
            Цена единицы дополнительно поставляемого Товара или цена единицы Товара при уменьшении предусмотренного Договором количества поставляемого Товара должна определяться как частное от деления первоначальной цены Договора на предусмотренное в Договоре количество Товара.<br/> 
            """
    story.append(Paragraph(text, style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("3. СРОКИ ДЕЙСТВИЯ ДОГОВОРА", style_bold))
    text = f"""Договор вступает в силу со дня его подписания обеими Сторонами. Срок действия договора c момента заключения Договора до {document.contract_lifetime}, в части расчетов до полного исполнения своих обязательств."""
    story.append(Paragraph(text, style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("4. СРОКИ И ПОРЯДОК ПОСТАВКИ ТОВАРА", style_bold))
    text = f"""4.1. Поставка Товара осуществляется со склада Поставщика транспортом Поставщика.<br/>
            4.2. Поставщик осуществляет передачу в течение 10 (десяти) рабочих дней со дня заключения контракта. Поставщик за 2 (два) дня до момента поставки товара информирует Заказчика о предстоящей поставке.<br/>
            4.3. Проверка качества Товара производится Заказчиком при его получении от Поставщика.<br/>
            4.4. Доставка Товара осуществляется силами Поставщика на склад Заказчика по адресу: {document.contract_place}<br/>      
            """
    story.append(Paragraph(text, style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("5. УПАКОВКА, МАРКИРОВКА И ПЕРЕДАЧА ТОВАРА", style_bold))
    text = """5.1. Товар поставляется в стандартной упаковке, отвечающей международным требованиям и обеспечивающей полную сохранность груза при условии надлежащего обращения с ним при транспортировке.<br/>
        5.2. Товар должен   быть   надлежащего   качества, соответствовать   стандартам, техническим условиям и иным требованиям к его качеству. С поставляемым Товаром Поставщик обязан предоставить сертификат соответствия, регистрационное удостоверение.<br/>
        5.3. В процессе приема-передачи Товара проверяется его комплектность и маркировка изделий.<br/>
        """
    story.append(Paragraph(text, style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("6. ПРАВО СОБСТВЕННОСТИ", style_bold))
    story.append(Paragraph("6.1. Право собственности на Товар переходит от Поставщика к Заказчику после приемки товара Заказчиком.",style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("7. ФОРС-МАЖОР", style_bold))
    story.append(Paragraph("7.1. Сторона освобождается от ответственности за частичное или полное неисполнение обязательств по настоящему Договору, если это неисполнение явилось следствием обстоятельств непреодолимой силы, возникших после заключения настоящего Договора в результате событий, которые сторона не могла предвидеть и предотвратить разумными мерами.",style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("8. ОТВЕТСТВЕННОСТЬ СТОРОН", style_bold))
    text = f"""8.1. Стороны несут ответственность за неисполнение либо ненадлежащее исполнение своих обязательств по настоящему договору.<br/>
                8.2. Стороны обязаны незамедлительно информировать друг друга об изменении указанных в договоре реквизитов, включая изменения фактических, почтовых и юридических адресов, а также уполномоченных представителей, предстоящих реорганизациях, ликвидациях и иных действиях, в результате которых может быть прекращена деятельность сторон или затруднено исполнение предусмотренных договором обязательств.<br/>
                8.3. Ни одна из сторон не имеет права в рамках настоящего Договора передавать свои права и обязательства третьей стороне без письменного подтверждения другой стороны.<br/>
                8.4. Пеня начисляется за каждый день просрочки исполнения обязательства Поставщиком, предусмотренного договором, в размере одной трехсотой действующей на дату уплаты пени ставки рефинансирования Центрального банка Российской Федерации от цены договора, уменьшенной на сумму, пропорциональную объему обязательств, предусмотренных договором и фактически исполненных Поставщиком.<br/>
                8.5. За каждый факт неисполнения или ненадлежащего исполнения Поставщиком обязательств, предусмотренных договором, за исключением просрочки исполнения обязательств (в том числе гарантийного обязательства), предусмотренных договором, размер штрафа устанавливается в виде фиксированной суммы, определяемой в следующем порядке:<br/>
                а) 10 процентов цены договора в случае, если цена договора не превышает 3 млн. рублей;<br/>
                8.6. Поставщик несет ответственность за качественное оказание Услуг в полном объеме и сроки установленные законодательством РФ.<br/>
                8.7. Пеня начисляется за каждый день просрочки исполнения ЗАКАЗЧИКОМ обязательства, предусмотренного Договором, начиная со дня, следующего после дня истечения установленного Договором срока исполнения обязательства. Такая пеня устанавливается Договором в размере одной трехсотой действующей на дату уплаты пеней ключевой ставки Центрального банка Российской Федерации от не уплаченной в срок суммы.<br/> 
                8.8. За каждый факт неисполнения Заказчиком обязательств, предусмотренных Договором, за исключением просрочки исполнения обязательств, предусмотренных Договором, размер штрафа устанавливается в виде фиксированной суммы - 1000 рублей.<br/>
                8.9.  Заключая настоящий Договор, Поставщик декларирует, что он соответствует требованиям к участникам закупки, установленным ч.1 ст. 31 Федерального закона от 05.04.2013г. {document.law_number} «О контрактной системе в сфере закупок товаров, работ, услуг для обеспечения государственных и муниципальных нужд»<br/>
            """
    story.append(Paragraph(text, style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("9. ГАРАНТИЙНЫЕ ОБЯЗАТЕЛЬСТВА", style_bold))
    story.append(Paragraph(f"9.1. Поставщик гарантирует качество и надежность поставленного товара в течение срока годности (прописанного в паспорте или инструкции по эксплуатации) с момента передачи товара Заказчику.",style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("10. РАЗРЕШЕНИЕ СПОРОВ", style_bold))
    text = """10.1. Все споры и разногласия, возникающие из настоящего Договора или в связи с ним, будут по возможности решаться путем переговоров.<br/>
                10.2. В случае недостижения взаимного согласия споры по настоящему Контракту разрешаются в Арбитражном суде Пермского края.<br/>
                До передачи спора на разрешение Арбитражного суда Пермского края Стороны примут меры к его урегулированию в претензионном порядке. Претензия должна быть направлена в письменном виде. По полученной претензии Сторона должна дать письменный ответ, по существу, в срок не позднее 14 (четырнадцати) дней с даты ее получения.<br/>
                10.3. Расторжение Договора допускается по соглашению Сторон, по решению суда, в случае одностороннего отказа Стороны Договора от исполнения Договора в соответствии с гражданским законодательством.<br/>
            """
    story.append(Paragraph(text, style))
    story.append(Paragraph("<br/>\n<br/>", style))

    text = """Приложение №1 - Техническое задание;<br/>
                Приложение №2 - Спецификация;<br/>
                Приложение №3 - Порядок приемки Товара;<br/>
                Приложение №4 - Форма документа о приемке Товара;<br/>
            """
    story.append(Paragraph(text, style))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("11. ЮРИДИЧЕСКИЕ АДРЕСА И РЕКВИЗИТЫ СТОРОН", style_bold))
    data = [
        [
            Paragraph(f"""
            ПОСТАВЩИК<br/>
            {user1.company_name}<br/>
            Адрес: {user1.address}<br/>
            Телефон: {user1.phone} <br/>
            Р/счет:	{user1.checking_account} <br/>  
            БИК: {user1.BIC} <br/>
            ИНН {user1.INN} <br/>
            КПП {user1.KPP} <br/>
            E-mail: {user1.email} <br/>
            <br/>\n<br/>
            <br/>\n<br/>
            <br/>\n<br/>
        """, style),
            Paragraph(f"""
            ЗАКАЗЧИК <br/>
            {user2.company_name}<br/>
            Адрес: {user2.address}<br/>
            Телефон: {user2.phone} <br/>
            Р/счет:	{user2.checking_account} <br/>  
            БИК: {user2.BIC} <br/>
            ИНН {user2.INN} <br/>
            КПП {user2.KPP} <br/>
            ОГРН {user2.OGRN} <br/>
            ОКПО {user2.OKPO}  <br/>
            e-mail: {user2.email} <br/>
        """, style)
        ]
    ]

    table = Table(data, colWidths=[8 * cm, 8 * cm])

    table_style = TableStyle([
        ('hAlign', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'TMR'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.transparent),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(table_style)
    story.append(table)

    story.append(Paragraph("<br/>\n<br/>", style))

    sign_table = Table([
        [
            Paragraph("Поставщик", style),
            Paragraph("Заказчик", style)
        ],
        [
            Paragraph("____________________", style),
            Paragraph("____________________", style)
        ]
    ], colWidths=[8 * cm, 8 * cm])

    sign_table_style = TableStyle([
        ('hAlign', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'TMR'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.transparent),
        ('GRID', (0, 0), (-1, -1), 1, colors.transparent)
    ])

    sign_table.setStyle(sign_table_style)
    story.append(sign_table)
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(PageBreak())

    story.append(Paragraph("Часть 2", left_allign_bold))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("1. Условия поставки", left_allign_bold))
    text = f"""1.1. Товар поставляется согласно техническому заданию в течение 10 рабочих дней со дня заключения контракта. Поставщик за 2 (два) дня до момента поставки товара информирует Заказчика о предстоящей поставке.<br/>
                1.2. Поставка осуществляется по адресу: {document.contract_place}.
            """
    story.append(Paragraph(text, left_allign))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("2. Требования к качеству продукции", left_allign_bold))
    text = """2.1. Товар должен быть сертифицирован или декларирован, иметь свидетельство о государственной регистрации (при наличии), регистрационное удостоверение.<br/>
            2.2. Товар должен полностью соответствовать стандартам качества, сертификату соответствия, техническому паспорту завода-изготовителя или технической спецификации завода изготовителя.<br/>
            2.3. Товар должен быть произведен при соблюдении требований нормативных документов (стандарты, технические условия, сертификаты качества и т.п.) в условиях их серийного производства.<br/>
            """
    story.append(Paragraph(text, left_allign))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("3. Требования к безопасности продукции", left_allign_bold))
    text = """3.1. Товар должен являться собственностью поставщика, не заложен, не арестован, не являться предметом третьих лиц.<br/>
            3.2. Товар должен быть новым (не бывшем в употреблении, не восстановленным).<br/>
            3.3. Товар должен быть упакован в тару, отвечающую требованиям ТУ и обеспечивающую его сохранность при перевозке и хранении. Год выпуска товара не ранее 2022 г.<br/>
            3.4. Маркировка упаковки (первичной и вторичной) должна соответствовать требованиям (нанесение на упаковку всей необходимой информации на русском языке).<br/>
            3.5. Остаточный срок годности на товар начинает действовать с момента передачи товара Заказчику и должен составлять не менее 24 месяцев.<br/>
            3.6. При поставке товара должны быть предоставлены все документы, подтверждающие качество товара (регистрационное удостоверение, свидетельство государственной регистрации (при наличии), сертификат или декларация соответствия(при их наличии), так же в сопроводительных документах (товарной накладной, реестре и т. п.) должны быть указаны серия (партия) и срок годности товара.<br/>
            3.7. Перед поставкой товара поставщик должен провести мониторинг безопасности изделия медицинского назначения (проверка товара, партии и т.д. по информационным письмам на сайте Росздравнадзора) в случае, если после поставки товара и дальнейшего мониторинга безопасности выявлены несоответствия, товар должен быть заменен на безопасный в течение трех дней.<br/>
            """
    story.append(Paragraph(text, left_allign))
    story.append(PageBreak())

    story.append(Paragraph("Приложение №1", right_allign))
    story.append(Paragraph("К настоящему договору", right_allign))
    story.append(Paragraph("<br/>\n<br/>", style))

    story.append(Paragraph("Спецификация", style_bold))

    product_table = Table([
        [
            Paragraph("№п/п", style),
            Paragraph("Наименование продукции", style),
            Paragraph("Ед.изм.", style),
            Paragraph("Цена за ед. в руб. (без НДС)", style),
            Paragraph("Количество", style),
            Paragraph("Сумма в руб. (без НДС)", style)
        ],
        [
            Paragraph("1", style),
            Paragraph("Игрушка-Елочка (Зеленая)", style),
            Paragraph("Штука", style),
            Paragraph("100", style),
            Paragraph("3", style),
            Paragraph("300", style)
        ]
    ])

    product_table_style = TableStyle([
        ('hAlign', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'TMR'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.transparent),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    product_table.setStyle(product_table_style)
    story.append(product_table)

    doc.build(story)

    return "backend/api/documents/generated/hackcontract.pdf"


