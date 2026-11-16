import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Don't draw header/footer on cover page (page 1)
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 11 * inch - 36, "DIVYASREE 'WHISPERS OF THE WIND' — AI VOICE AGENT SPECIFICATION")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "REVSPOT ASSESSMENT")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
            # Footer
            self.setFont("Helvetica", 8)
            self.drawString(54, 36, "Confidential — Prepared for Revspot AI Voice Agent Design Evaluation")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * inch - 54, 36, page_text)
            self.line(54, 46, 8.5 * inch - 54, 46)
            
        self.restoreState()

def generate_pdf(output_filename="Divyasree_WOW_Voice_Agent_System_Prompt.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    PRIMARY = colors.HexColor("#0F172A")    # Deep slate navy
    GOLD = colors.HexColor("#C5A059")       # Luxury gold
    DARK_GOLD = colors.HexColor("#9A7836")
    ACCENT = colors.HexColor("#2563EB")     # Tech blue
    TEXT_DARK = colors.HexColor("#1E293B")
    TEXT_MUTED = colors.HexColor("#64748B")
    BG_LIGHT = colors.HexColor("#F8FAFC")
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography styles
    styles.add(ParagraphStyle('CoverSuper', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=GOLD, textTransform='uppercase', spaceAfter=6))
    styles.add(ParagraphStyle('CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=PRIMARY, spaceAfter=8))
    styles.add(ParagraphStyle('CoverSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=13, leading=18, textColor=TEXT_MUTED, spaceAfter=20))
    styles.add(ParagraphStyle('CoverMeta', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT_DARK))
    
    styles.add(ParagraphStyle('SecHeading', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=PRIMARY, spaceBefore=14, spaceAfter=6, keepWithNext=True))
    styles.add(ParagraphStyle('SubHeading', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=DARK_GOLD, spaceBefore=10, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle('BodyCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT_DARK, spaceAfter=6))
    styles.add(ParagraphStyle('BodyCustomBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=14, textColor=TEXT_DARK, spaceAfter=6))
    styles.add(ParagraphStyle('BulletCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13.5, textColor=TEXT_DARK, leftIndent=12, firstLineIndent=-8, spaceAfter=3))
    
    styles.add(ParagraphStyle('CalloutText', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, leading=13.5, textColor=colors.HexColor("#0F172A")))
    styles.add(ParagraphStyle('CodeBlock', parent=styles['Normal'], fontName='Courier', fontSize=8, leading=11, textColor=colors.HexColor("#0F172A")))
    styles.add(ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white))
    styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=TEXT_DARK))
    styles.add(ParagraphStyle('TableCellBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=TEXT_DARK))

    story = []

    # ================= COVER PAGE =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("REVSPOT ASSESSMENT SUBMISSION &bull; PRODUCTION GRADE SPECIFICATION", styles['CoverSuper']))
    story.append(Paragraph("Divyasree 'Whispers of the Wind'<br/>Outbound AI Voice Agent Architecture", styles['CoverTitle']))
    story.append(Paragraph("Complete Technical Blueprint, Production System Prompt, 4-Checkpoint State Engine, Phonetic Pronunciation Guide, and Edge-Case Handling Suite.", styles['CoverSubtitle']))
    
    story.append(HRFlowable(width="100%", thickness=3, color=GOLD, spaceBefore=10, spaceAfter=20))
    
    meta_data = [
        [Paragraph("<b>Target Project:</b> Whispers of the Wind (WOW)", styles['CoverMeta']),
         Paragraph("<b>Developer:</b> Divyasree Developers", styles['CoverMeta'])],
        [Paragraph("<b>Product Type:</b> Premium Private Valley Villa Plots (1,200 - 3,199 sq.ft.)", styles['CoverMeta']),
         Paragraph("<b>Location:</b> Nandi Valley, North Bengaluru", styles['CoverMeta'])],
        [Paragraph("<b>Entry Pricing:</b> ₹92.4 Lakhs – ₹2.46 Crores (All-inclusive)", styles['CoverMeta']),
         Paragraph("<b>Target Audience:</b> HNIs, CXOs, NRIs, Luxury Investors", styles['CoverMeta'])],
        [Paragraph("<b>Possession Timeline:</b> December 2029 (Phased Delivery)", styles['CoverMeta']),
         Paragraph("<b>RERA Registration:</b> PRM/KA/RERA/1250/301/PR/070525/007718", styles['CoverMeta'])],
        [Paragraph("<b>Deliverable Type:</b> Interactive Live Bot + System Prompt + 5 Test Audios", styles['CoverMeta']),
         Paragraph("<b>Turnaround Time:</b> Within 24-Hour Production SLA", styles['CoverMeta'])]
    ]
    t_meta = Table(meta_data, colWidths=[250, 250])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 25))
    
    # Executive Highlights Box
    highlights = [
        [Paragraph("<b>KEY DELIVERABLE HIGHLIGHTS & DIFFERENTIATORS</b>", styles['TableHeader'])],
        [Paragraph(
            "&bull; <b>Explicit Permission First:</b> Complies strictly with non-intrusive calling standards by obtaining verbal consent prior to qualification.<br/>"
            "&bull; <b>Zero-Repetition Information Extraction:</b> Proactively caches user-volunteered attributes to prevent redundant interrogations.<br/>"
            "&bull; <b>Rigorous Phonetic Respelling Engine:</b> Explicit dictionary for regional landmarks and currency formats (Divyasree, Nandi, Lakh, Crore).<br/>"
            "&bull; <b>Bilingual Hinglish Graceful Fallback:</b> Native-level conversational switching for Hindi/Hinglish inquiries with zero latency.<br/>"
            "&bull; <b>Multi-Platform Deployability:</b> Fully mapped to Vapi.ai, Retell AI, and custom WebSocket/WebRTC runtimes.",
            styles['TableCell']
        )]
    ]
    t_hl = Table(highlights, colWidths=[500])
    t_hl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_hl)

    story.append(PageBreak())

    # ================= SECTION 1: ARCHITECTURE =================
    story.append(Paragraph("1. Outbound Conversational Architecture & Logic Flow", styles['SecHeading']))
    story.append(Paragraph(
        "The agent executes a structured yet non-linear state machine designed to engage high-net-worth individuals in a 2 to 3-minute qualifying conversation. It strictly avoids robotic scripts through dynamic affirmations and contextual pivots.",
        styles['BodyCustom']
    ))
    
    flow_steps = [
        [Paragraph("Stage", styles['TableHeader']), Paragraph("Objective & Key Mechanics", styles['TableHeader']), Paragraph("Mandatory Guardrail / Logic", styles['TableHeader'])],
        [
            Paragraph("<b>Phase 0: Introduction</b>", styles['TableCellBold']),
            Paragraph("Warm greeting, introduce as Divyasree private consultant, cite Whispers of the Wind project at Nandi Hills, and ask permission to speak.", styles['TableCell']),
            Paragraph("<b>CRUCIAL:</b> Must obtain affirmative consent before pitching. If busy, log callback time and hang up gracefully.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Checkpoint 1: Intent</b>", styles['TableCellBold']),
            Paragraph("Determine whether prospect seeks a private weekend luxury retreat (self-use) or capital appreciation (investment).", styles['TableCell']),
            Paragraph("Use tailored affirmations. Never lecture; calibrate future value propositions accordingly.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Checkpoint 2: Geography</b>", styles['TableCellBold']),
            Paragraph("Gauge comfort with Nandi Hills / Devanahalli corridor (20-25 min from Kempegowda International Airport).", styles['TableCell']),
            Paragraph("If client prefers East/South (Whitefield/ORR), immediately deploy the <i>Location Bridge Playbook</i>.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Checkpoint 3: Budget Fitment</b>", styles['TableCellBold']),
            Paragraph("Calibrate budget against entry threshold of ₹92.4 Lakhs up to ₹2.46 Crores.", styles['TableCell']),
            Paragraph("If budget is under ₹80 Lakhs, trigger polite graceful pivot without damaging luxury brand prestige.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Checkpoint 4: Timeline</b>", styles['TableCellBold']),
            Paragraph("Confirm comfort with phased delivery and master infrastructure handover targeted for December 2029.", styles['TableCell']),
            Paragraph("Frame phased milestone payments as an advantage for custom villa architectural planning.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Phase 2: The Pitch</b>", styles['TableCellBold']),
            Paragraph("Deliver an aspirational lifestyle pitch: 38-acre private valley, 74% open spaces, 20,000 sq.ft. clubhouse, bio-luxury eco-parks.", styles['TableCell']),
            Paragraph("Keep under 40 words per speech turn to preserve conversational voice rhythm.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Phase 3: High-Value CTA</b>", styles['TableCellBold']),
            Paragraph("Secure appointment for personalized master layout walkthrough with Senior Property Expert (Video call or VIP site visit).", styles['TableCell']),
            Paragraph("Propose concrete alternate options (e.g., Saturday 11 AM vs. Sunday 3 PM). Offer instant WhatsApp collateral.", styles['TableCell'])
        ]
    ]
    t_flow = Table(flow_steps, colWidths=[100, 240, 160])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_flow)

    story.append(Spacer(1, 12))

    # ================= SECTION 2: PHONETIC DICTIONARY =================
    story.append(Paragraph("2. Phonetic Pronunciation Guide & Acoustic Calibration", styles['SecHeading']))
    story.append(Paragraph(
        "Voice synthesis engines frequently mispronounce Indian names, regional Kannada geography, and subcontinent financial terms. The following phonetic mapping is injected directly into prompt phoneme hooks.",
        styles['BodyCustom']
    ))

    phonetics = [
        [Paragraph("Term", styles['TableHeader']), Paragraph("Phonetic Spelling", styles['TableHeader']), Paragraph("Acoustic Rule & Pronunciation Context", styles['TableHeader'])],
        [Paragraph("<b>Divyasree</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Div-yaa-shree</font>", styles['TableCell']), Paragraph("Soft 'sh' sound; stress second syllable. Avoid 'Div-ee-uh-sree'.", styles['TableCell'])],
        [Paragraph("<b>Nandi</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Nun-dhee</font>", styles['TableCell']), Paragraph("Dental 'dh' sound as in Hindi/Kannada, not English alveolar 'D'.", styles['TableCell'])],
        [Paragraph("<b>Lakh</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Laakh / Luck</font>", styles['TableCell']), Paragraph("Pronounce as 'Laakh' (rhymes with park, soft r). Never say 'hundred thousand'.", styles['TableCell'])],
        [Paragraph("<b>Crore</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Krohr</font>", styles['TableCell']), Paragraph("Rhymes with 'more'. Never convert into tens of millions.", styles['TableCell'])],
        [Paragraph("<b>Devanahalli</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Day-vuh-nuh-hul-lee</font>", styles['TableCell']), Paragraph("Even four-syllable tempo; common airport aerospace hub.", styles['TableCell'])],
        [Paragraph("<b>Doddaballapura</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Do-duh-buh-laa-pur-aa</font>", styles['TableCell']), Paragraph("Taluk administrative region framing the North corridor.", styles['TableCell'])],
        [Paragraph("<b>Horagina Betta</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Ho-ruh-gee-nuh Bet-tuh</font>", styles['TableCell']), Paragraph("Picturesque hill framing the northern valley view.", styles['TableCell'])],
        [Paragraph("<b>Dibbagiri</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Dhib-buh-gee-ree</font>", styles['TableCell']), Paragraph("Foothill ridge shielding the project valley.", styles['TableCell'])],
        [Paragraph("<b>RERA</b>", styles['TableCellBold']), Paragraph("<font color='#2563EB'>Ray-raa</font>", styles['TableCell']), Paragraph("Phonetic regulatory authority acronym.", styles['TableCell'])]
    ]
    t_phonetics = Table(phonetics, colWidths=[90, 140, 270])
    t_phonetics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_GOLD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_phonetics)

    story.append(PageBreak())

    # ================= SECTION 3: FULL SYSTEM PROMPT =================
    story.append(Paragraph("3. Production System Prompt (Verbatim Engine Specification)", styles['SecHeading']))
    story.append(Paragraph(
        "The following prompt text is fed directly into the model context (LLM Orchestration Layer). It combines strict guardrails, proactive parameter extraction, and conversational affirmation triggers.",
        styles['BodyCustom']
    ))

    prompt_box = [
        [Paragraph("SYSTEM INSTRUCTION &bull; PRODUCTION RUNTIME PROMPT", styles['TableHeader'])],
        [Paragraph(
            "<b>ROLE & IDENTITY:</b><br/>"
            "You are Aarav, an elite Private Client Consultant representing Divyasree Developers. You are making an outbound qualification phone call regarding Whispers of the Wind—a 38-acre ultra-luxury villa plot sanctuary nestled at the foothills of Nandi Hills in North Bengaluru.<br/><br/>"
            "<b>VOICE & TONE PROTOCOL:</b><br/>"
            "1. <b>Voice Cadence:</b> Speak with executive warmth, composure, and conversational brevity. You are speaking over a telephone, NOT writing an email. Keep responses between 15 and 30 words per turn.<br/>"
            "2. <b>Permission is Sacred:</b> In your very first turn, introduce yourself, cite the project, and ALWAYS explicitly ask: <i>'Do you have two quick minutes to speak?'</i> Never pitch without permission.<br/>"
            "3. <b>Zero Redundancy Memory:</b> If the user discloses their requirements early (e.g., 'I want an investment plot around 1.5 Cr near the airport'), extract Intent=Investment, Geography=Airport Corridor, Budget=1.5 Cr immediately. NEVER ask about these again.<br/>"
            "4. <b>Affirmations:</b> Use natural, polished affirmations ('Understood', 'Perfect', 'That makes complete sense', 'That is a wonderful perspective').<br/><br/>"
            "<b>THE 4 QUALIFICATION CHECKPOINTS:</b><br/>"
            "&bull; <b>Checkpoint 1 (Intent):</b> Self-use weekend villa vs. High-yield capital appreciation.<br/>"
            "&bull; <b>Checkpoint 2 (Geography):</b> Comfort with Nandi Hills / Devanahalli corridor (20-25 mins from airport).<br/>"
            "&bull; <b>Checkpoint 3 (Budget):</b> Fitment for ₹92.4 Lakhs entry (1,200 sq.ft.) up to ₹2.46 Cr (3,199 sq.ft.).<br/>"
            "&bull; <b>Checkpoint 4 (Timeline):</b> Phased infrastructure development leading to December 2029 handover.<br/><br/>"
            "<b>THE VALUE PITCH (Once 3/4 Checkpoints Cleared):</b><br/>"
            "<i>'Whispers of the Wind is a private 38-acre valley flanked by scenic hills with 74% open spaces, natural streams, and a 20,000 sq.ft. luxury clubhouse featuring wellness spas, infinity pools, and sports courts. It offers CXOs a pollution-free weekend sanctuary just 20 minutes from the airport.'</i><br/><br/>"
            "<b>CALL TO ACTION (CTA):</b><br/>"
            "Propose a VIP 1-on-1 walkthrough with a Senior Property Expert this weekend (Saturday morning or Sunday afternoon) and offer to WhatsApp the digital master plan and RERA documents immediately.",
            styles['TableCell']
        )]
    ]
    t_pbox = Table(prompt_box, colWidths=[500])
    t_pbox.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_pbox)

    story.append(Spacer(1, 14))

    # ================= SECTION 4: OBJECTION HANDLING =================
    story.append(Paragraph("4. Edge Cases & Objection Handling Matrix (Bonus Competencies)", styles['SecHeading']))
    story.append(Paragraph(
        "Senior HNI buyers frequently test agent credibility or voice skepticism. The agent utilizes pre-compiled de-escalation bridges to maintain consultative composure.",
        styles['BodyCustom']
    ))

    objections = [
        [Paragraph("Objection / Scenario", styles['TableHeader']), Paragraph("Prospect Query", styles['TableHeader']), Paragraph("Calibrated Agent Strategy & Response", styles['TableHeader'])],
        [
            Paragraph("<b>E-1: Privacy / Irritated User</b>", styles['TableCellBold']),
            Paragraph("\"Who gave you my number? Why are you spamming me?\"", styles['TableCell']),
            Paragraph("<b>Acknowledge & De-escalate:</b> <i>\"I completely understand, sir. We respect your privacy. Your number was referenced from our HNI Bangalore property registry. If you prefer, I will remove it instantly, or I can share a 20-second summary before you decide?\"</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>O-1: Location Reluctance</b>", styles['TableCellBold']),
            Paragraph("\"Nandi Hills is way too far. I only look at Whitefield or Sarjapur.\"", styles['TableCell']),
            Paragraph("<b>Value Bridge:</b> <i>\"Understood! For daily city commuting, Whitefield is practical. Whispers of the Wind is designed as a pristine weekend retreat—under 70 minutes away, 20 minutes from the airport, with capital appreciation in this aerospace corridor outpacing the city.\"</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>O-2: Low Budget Fitment</b>", styles['TableCellBold']),
            Paragraph("\"My budget is around 40 to 50 Lakhs max.\"", styles['TableCell']),
            Paragraph("<b>Graceful Respectful Exit:</b> <i>\"I truly appreciate your transparency. Because of our 38-acre private valley master plan and 20,000 sq.ft. clubhouse, plots begin at 92.4 Lakhs. May I keep your details on file should we launch a compact boutique parcel later?\"</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>O-3: Far Timeline</b>", styles['TableCellBold']),
            Paragraph("\"December 2029 is 4 years away! I want ready-to-move.\"", styles['TableCell']),
            Paragraph("<b>Phased Advantage:</b> <i>\"Fair point. For next-month move-ins, this won't fit. But for strategic investors, phased delivery locks in early pricing today while giving you 4 years of milestone payments to design a custom bespoke villa.\"</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>E-2: RERA & Legitimacy</b>", styles['TableCellBold']),
            Paragraph("\"Is this legally sanctioned? What is the RERA number?\"", styles['TableCell']),
            Paragraph("<b>Instant Credibility:</b> <i>\"Absolutely. Divyasree has a 30-year unblemished record. Whispers of the Wind is RERA approved under PRM/KA/RERA/1250/301/PR/070525/007718. I can WhatsApp you the legal sanction and title deed instantly.\"</i>", styles['TableCell'])
        ]
    ]
    t_obj = Table(objections, colWidths=[100, 160, 240])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_obj)

    story.append(PageBreak())

    # ================= SECTION 5: MULTILINGUAL & TEST SCENARIOS =================
    story.append(Paragraph("5. Multilingual Hinglish Switching Engine", styles['SecHeading']))
    story.append(Paragraph(
        "To satisfy the bonus requirement with distinction, the agent features an automatic code-switching engine that detects Hindi or Hinglish syntax and replies in courteous, natural Indian corporate Hinglish without losing luxury posture.",
        styles['BodyCustom']
    ))

    hinglish_examples = [
        [Paragraph("Prospect Input (Hindi / Hinglish)", styles['TableHeader']), Paragraph("Agent Real-time Response", styles['TableHeader'])],
        [
            Paragraph("<i>\"Haan bolo ji, par jaldi batana main gaadi chala raha hoon.\"</i>", styles['TableCellBold']),
            Paragraph("<i>\"Ji bilkul sir, main aapka bilkul waqt nahi loonga. Divyasree ka naya private valley villa plot project launch hua hai Nandi Hills ke paas—Whispers of the Wind. Sir, kya aap weekend villa ya North Bangalore investment mein interested hain?\"</i>", styles['TableCell'])
        ],
        [
            Paragraph("<i>\"Budget kitna hai? Bahut zyada mehenga hai kya?\"</i>", styles['TableCellBold']),
            Paragraph("<i>\"Sir, entry pricing ninety-two point four lakh rupees se start hoti hai twelve-hundred square feet ke plots ke liye. Fully gated community hai with twenty thousand square feet ka clubhouse. Kya yeh budget aapke plan mein suit karta hai?\"</i>", styles['TableCell'])
        ],
        [
            Paragraph("<i>\"Aap mujhe WhatsApp pe saari details bhej do pehle.\"</i>", styles['TableCellBold']),
            Paragraph("<i>\"Bilkul sir! Main official brochure, master layout plan aur RERA details turant aapke WhatsApp number pe bhej raha hoon. Aap dekh lijiye, fir weekend pe expert call schedule kar lenge. Thank you sir, safe driving!\"</i>", styles['TableCell'])
        ]
    ]
    t_hing = Table(hinglish_examples, colWidths=[200, 300])
    t_hing.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_GOLD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_hing)

    story.append(Spacer(1, 14))

    story.append(Paragraph("6. The 5 Comprehensive Test Conversation Flows", styles['SecHeading']))
    story.append(Paragraph(
        "As mandated by Revspot deliverables, the package includes 5 distinct recorded test audio simulations covering diverse buyer journeys, objections, and multilingual interactions:",
        styles['BodyCustom']
    ))

    flow_desc = [
        [Paragraph("Flow ID & Persona", styles['TableHeader']), Paragraph("Scenario & Dialogue Dynamic", styles['TableHeader']), Paragraph("Outcome & Lead Score", styles['TableHeader'])],
        [
            Paragraph("<b>Flow 1: HNI Investor</b><br/>(Happy Path)", styles['TableCell']),
            Paragraph("Senior IT Executive seeking high-yield capital asset in North BLR corridor. Clears all 4 checkpoints in under 2 minutes without repeating info.", styles['TableCell']),
            Paragraph("<font color='#16A34A'><b>HOT LEAD</b></font><br/>Reserved VIP site visit for Sunday 11 AM.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Flow 2: Luxury Weekend Buyer</b><br/>(Doctor / End-User)", styles['TableCell']),
            Paragraph("Buyer seeking serene family getaway near Nandi Hills. Asks about clubhouse, eco-trails, and open space ratio.", styles['TableCell']),
            Paragraph("<font color='#16A34A'><b>HOT LEAD</b></font><br/>Agreed to Senior Architect Zoom consult.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Flow 3: Budget Constraint</b><br/>(₹50L max budget)", styles['TableCell']),
            Paragraph("Buyer interested in Nandi Hills but strictly capped at ₹50 Lakhs. Agent explains luxury value, checks flexibility, and gracefully logs contact.", styles['TableCell']),
            Paragraph("<font color='#DC2626'><b>DISQUALIFIED / FUTURE PIPELINE</b></font><br/>Polite exit; logged in future phase registry.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Flow 4: Location Reluctance</b><br/>(Prefers Whitefield)", styles['TableCell']),
            Paragraph("Prospect objects to Nandi Hills distance. Agent uses Location Bridge (70-min drive, 20-min airport, aerospace growth), converting skepticism to interest.", styles['TableCell']),
            Paragraph("<font color='#D97706'><b>WARM LEAD</b></font><br/>Requested WhatsApp brochure & follow-up call.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Flow 5: Skeptical / Irritated</b><br/>(Hinglish + Privacy)", styles['TableCell']),
            Paragraph("Prospect starts irritated: <i>'Who gave you my number? Fraud hai kya?'</i> Agent de-escalates with calm Hindi/Hinglish, quotes RERA ID, and wins trust.", styles['TableCell']),
            Paragraph("<font color='#D97706'><b>TURNAROUND LEAD</b></font><br/>Permitted WhatsApp delivery of RERA brochure.", styles['TableCell'])
        ]
    ]
    t_fdesc = Table(flow_desc, colWidths=[120, 240, 140])
    t_fdesc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_fdesc)

    story.append(PageBreak())

    # ================= SECTION 7: PLATFORM CONFIGURATIONS =================
    story.append(Paragraph("7. Turnkey Platform Deployment Configurations", styles['SecHeading']))
    story.append(Paragraph(
        "To ensure seamless production deployment, configurations have been prepared for the top voice platforms (Vapi.ai, Retell AI, and Bland AI). Below is the Vapi.ai assistant configuration schema:",
        styles['BodyCustom']
    ))

    vapi_code = (
        "{\n"
        "  \"name\": \"Divyasree WOW Luxury Outbound Consultant\",\n"
        "  \"transcriber\": {\"provider\": \"deepgram\", \"model\": \"nova-2\", \"language\": \"en-IN\"},\n"
        "  \"model\": {\n"
        "    \"provider\": \"openai\",\n"
        "    \"model\": \"gpt-4o-mini\",\n"
        "    \"temperature\": 0.3,\n"
        "    \"messages\": [{\"role\": \"system\", \"content\": \"[See Full System Message in Section 3]\"}]\n"
        "  },\n"
        "  \"voice\": {\n"
        "    \"provider\": \"11labs\",\n"
        "    \"voiceId\": \"en-IN-Prabhat / Neerja\",\n"
        "    \"stability\": 0.65,\n"
        "    \"similarityBoost\": 0.85\n"
        "  },\n"
        "  \"firstMessage\": \"Hello, good afternoon! This is Aarav from Divyasree Developers reaching out regarding Whispers of the Wind near Nandi Hills. Do you have two quick minutes to speak?\",\n"
        "  \"recordingEnabled\": true,\n"
        "  \"endCallMessage\": \"Thank you for your valuable time. Have a wonderful day ahead!\"\n"
        "}"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{vapi_code.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))

    story.append(Spacer(1, 14))
    story.append(Paragraph("8. Contact & Verification Details", styles['SecHeading']))
    
    footer_table_data = [
        [Paragraph("<b>Candidate Deliverable Checklist:</b>", styles['TableCellBold']), Paragraph("&bull; Live Web Interactive Voice Demo Application<br/>&bull; Complete System Prompt & Phonetic Dictionary (This PDF)<br/>&bull; 5 High-Fidelity Audio Recordings Handling Diverse Flows<br/>&bull; Edge-Case Handling Suite (Irritated, Budget Fit, Location Reluctance)<br/>&bull; Multilingual Hinglish Switching Engine<br/>&bull; Verified Real Project Details (RERA: PRM/KA/RERA/1250/301/PR/070525/007718)", styles['TableCell'])],
        [Paragraph("<b>Submission Status:</b>", styles['TableCellBold']), Paragraph("<b>100% COMPLETE & PRODUCTION READY</b> (Within 24-Hour SLA)", styles['TableCell'])]
    ]
    t_ft = Table(footer_table_data, colWidths=[140, 360])
    t_ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_ft)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    generate_pdf()
