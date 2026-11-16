import re
import json

class VoiceAgentEngine:
    """
    Intelligent conversational engine for Divyasree 'Whispers of the Wind' outbound voice qualification.
    Maintains a deterministic 4-checkpoint state machine with proactive extraction,
    natural language affirmations, multilingual code-switching, and objection handling.
    """
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.state = {
            "permission_granted": None,   # True / False / None
            "checkpoint_1_intent": None,  # "Self-Use" | "Investment" | "Dual" | None
            "checkpoint_2_geography": None, # "Comfortable" | "Reluctant" | "Convinced" | None
            "checkpoint_3_budget": None,  # "Qualified" | "Stretched" | "Disqualified" | None
            "checkpoint_4_timeline": None,# "Aligned" | "Immediate" | "Flexible" | None
            "pitch_delivered": False,
            "cta_proposed": False,
            "appointment_scheduled": None,
            "language": "en",             # "en" | "hinglish"
            "sentiment": "Neutral",       # "Receptive" | "Enthusiastic" | "Skeptical" | "Irritated" | "Busy"
            "lead_score": 50,             # 0 to 100
            "lead_status": "WARM",        # "HOT" | "WARM" | "DISQUALIFIED"
            "call_stage": "INTRO"         # "INTRO" | "QUALIFYING" | "PITCH" | "CTA" | "CLOSED"
        }
        self.history = []

    def calculate_score(self):
        score = 40
        if self.state["permission_granted"] is True:
            score += 10
        if self.state["checkpoint_1_intent"]:
            score += 15
        if self.state["checkpoint_2_geography"] in ["Comfortable", "Convinced"]:
            score += 15
        if self.state["checkpoint_3_budget"] == "Qualified":
            score += 20
        elif self.state["checkpoint_3_budget"] == "Disqualified":
            score = min(score, 35)
        if self.state["checkpoint_4_timeline"] in ["Aligned", "Flexible"]:
            score += 10
        if self.state["appointment_scheduled"]:
            score += 15
            
        score = min(100, max(0, score))
        self.state["lead_score"] = score
        
        if self.state["checkpoint_3_budget"] == "Disqualified":
            self.state["lead_status"] = "DISQUALIFIED"
        elif score >= 75:
            self.state["lead_status"] = "HOT LEAD"
        elif score >= 50:
            self.state["lead_status"] = "WARM LEAD"
        else:
            self.state["lead_status"] = "COLD / PENDING"

    def detect_language_and_sentiment(self, text):
        t = text.lower()
        # Hindi/Hinglish detection
        hindi_keywords = [
            "kya", "hai", "nahi", "kaun", "kahan", "bol", "bolo", "batao", "bhejo",
            "fraud", "gussa", "waqt", "shukriya", "dhanyawad", "acha", "theek",
            "bhai", "sir ji", "aapko", "mera", "paas", "kitna", "mehenga", "gaadi"
        ]
        if any(w in t for w in hindi_keywords):
            self.state["language"] = "hinglish"
            
        # Sentiment detection
        if any(w in t for w in ["fraud", "spam", "kahan se number mila", "who gave you my number", "stop calling", "dont call", "irritated", "disturb"]):
            self.state["sentiment"] = "Irritated / Skeptical"
        elif any(w in t for w in ["busy", "driving", "meeting", "call later", "cant talk", "baad me"]):
            self.state["sentiment"] = "Busy / Inconvenienced"
        elif any(w in t for w in ["great", "wonderful", "love", "sounds good", "interested", "perfect", "awesome", "badiya"]):
            self.state["sentiment"] = "Enthusiastic"
        elif any(w in t for w in ["yes", "sure", "tell me", "okay", "go ahead", "haan"]):
            self.state["sentiment"] = "Receptive"
        elif any(w in t for w in ["rera", "legal", "proof", "sanction", "approval"]):
            self.state["sentiment"] = "Inquiring / Verification"

    def process_turn(self, user_text):
        """
        Takes user voice/text transcript and generates contextually nuanced, state-tracked response.
        """
        self.detect_language_and_sentiment(user_text)
        t = user_text.lower()
        
        # Proactive Information Extraction
        # Intent extraction
        if any(w in t for w in ["investment", "invest", "returns", "appreciation", "roi", "asset"]):
            if not self.state["checkpoint_1_intent"]:
                self.state["checkpoint_1_intent"] = "Investment"
        if any(w in t for w in ["weekend", "family", "self use", "stay", "retire", "live", "villa", "peaceful", "escape"]):
            if not self.state["checkpoint_1_intent"]:
                self.state["checkpoint_1_intent"] = "Self-Use"
                
        # Geography extraction
        if any(w in t for w in ["nandi", "airport", "north bangalore", "devanahalli", "hebbal"]):
            if not self.state["checkpoint_2_geography"]:
                self.state["checkpoint_2_geography"] = "Comfortable"
        if any(w in t for w in ["whitefield", "sarjapur", "electronic city", "too far", "door hai", "east bangalore", "south bangalore"]):
            self.state["checkpoint_2_geography"] = "Reluctant"

        # Budget extraction
        if any(w in t for w in ["1 crore", "1.5", "2 crore", "crores", "1cr", "1.5cr", "2cr", "comfortable", "90 lakh", "92 lakh", "one crore", "two crore"]):
            self.state["checkpoint_3_budget"] = "Qualified"
        elif any(w in t for w in ["40 lakh", "50 lakh", "30 lakh", "under 50", "max 50", "45 lakh", "budget is low", "mehenga"]):
            if any(w in t for w in ["40", "50", "30", "45"]):
                self.state["checkpoint_3_budget"] = "Disqualified"

        # Timeline extraction
        if any(w in t for w in ["2029", "december 2029", "four years", "4 years", "fine", "suits", "matches", "long term"]):
            self.state["checkpoint_4_timeline"] = "Aligned"
        elif any(w in t for w in ["ready to move", "immediate", "next month", "urgent", "too long"]):
            self.state["checkpoint_4_timeline"] = "Immediate"

        # State Response Dispatcher
        reply = self._generate_response(t, user_text)
        self.calculate_score()
        
        self.history.append({"user": user_text, "agent": reply})
        return {
            "reply": reply,
            "state": self.state
        }

    def _generate_response(self, t, original_text):
        # 1. Handle Irritated / Privacy Skeptic (Edge Case E-1)
        if self.state["sentiment"] == "Irritated / Skeptical":
            if self.state["language"] == "hinglish":
                return "Sir, main aapka gussa aur concern bilkul samajh sakta hoon. Hum privacy ko bohot seriously lete hain. Agar aap interested nahi hain toh main turant apna call cut kar deta hoon, ya kya main thirty seconds mein project brief kar sakta hoon?"
            return "I completely understand your concern, and I respect your privacy. Your contact was referenced from our verified Bangalore property network. If you prefer not to be contacted, I will gladly remove your number immediately. Would you like me to delete it, or may I share a quick thirty-second brief before you decide?"

        # 2. Handle Busy / Reschedule
        if self.state["sentiment"] == "Busy / Inconvenienced":
            self.state["call_stage"] = "CLOSED"
            if self.state["language"] == "hinglish":
                return "Ji bilkul sir, main aapka waqt nahi loonga. Kya main aaj shaam ko ya kal subah do minute ke liye call kar sakta hoon?"
            return "I completely understand! I will not hold you. Would later this evening or tomorrow morning work better for a quick two-minute catch-up?"

        # 3. Handle RERA / Authenticity Inquiry (Edge Case E-2)
        if "rera" in t or "legal" in t or "approval" in t or "sanction" in t:
            if self.state["language"] == "hinglish":
                return "Whispers of the Wind hundred percent government approved hai! Iska Karnataka RERA number hai PRM slash KA slash RERA slash 1250 slash 301 slash PR slash 070525 slash 007718. Divyasree ka thirty years ka reputed record hai. Main direct RERA certificate aapko WhatsApp kar deta hoon!"
            return "Absolutely! Divyasree has a thirty-year unblemished record across South India. Whispers of the Wind is fully legally sanctioned and RERA registered under PRM slash KA slash RERA slash 1250 slash 301 slash PR slash 070525 slash 007718. All title documents and approvals are completely clear."

        # 4. Handle Location Objection (Objection O-1)
        if self.state["checkpoint_2_geography"] == "Reluctant" and not self.state["pitch_delivered"]:
            self.state["checkpoint_2_geography"] = "Convinced"
            return "That is a completely valid observation! For daily work commutes, Whitefield or East Bangalore makes total sense. Whispers of the Wind is designed not for daily travel, but as a private weekend sanctuary—under seventy minutes away via the Bellary expressway, and twenty minutes from the airport. Furthermore, the Satellite Town Ring Road and Aerospace SEZ are driving land appreciation here faster than the city. Does that perspective make sense?"

        # 5. Handle Low Budget Disqualification (Objection O-2)
        if self.state["checkpoint_3_budget"] == "Disqualified":
            self.state["call_stage"] = "CLOSED"
            return "I truly appreciate your transparency! Because of our thirty-eight acre private valley master plan, underground cabling, and twenty-thousand square foot clubhouse, entry plots start at ninety-two point four Lakhs. While Whispers of the Wind may be above your target, may I keep your details on file in case Divyasree introduces a boutique parcel later?"

        # 6. Check Initial Permission (Phase 0)
        if self.state["permission_granted"] is None:
            if any(w in t for w in ["yes", "sure", "tell me", "okay", "go ahead", "haan", "bolo", "what is it"]):
                self.state["permission_granted"] = True
                self.state["call_stage"] = "QUALIFYING"
                if not self.state["checkpoint_1_intent"]:
                    return "Wonderful, thank you! To ensure I share what is most relevant to you—are you currently exploring this more as a private weekend retreat for family, or are you looking at it primarily from a high-yield land investment perspective?"
            else:
                return "Hello! This is Aarav from Divyasree Developers reaching out regarding Whispers of the Wind near Nandi Hills. Do you have two quick minutes to speak?"

        # 7. Checkpoint 1: Intent
        if not self.state["checkpoint_1_intent"]:
            if "invest" in t:
                self.state["checkpoint_1_intent"] = "Investment"
            elif any(w in t for w in ["weekend", "family", "self", "stay", "villa"]):
                self.state["checkpoint_1_intent"] = "Self-Use"
            else:
                return "Understood. Would you be looking at this primarily as a serene weekend home for personal leisure, or are you exploring land capital appreciation near the airport corridor?"

        # 8. Checkpoint 2: Geography
        if not self.state["checkpoint_2_geography"]:
            return "Perfect! Whispers of the Wind is located in the scenic Nandi Valley, just twenty minutes past the International Airport. Have you been tracking the rapid infrastructure growth along the North Bengaluru corridor recently?"

        # 9. Checkpoint 3: Budget
        if not self.state["checkpoint_3_budget"]:
            return "In terms of configuration, our private valley plots range from twelve-hundred square feet up to larger signature estates, with entry pricing starting at ninety-two point four Lakh Rupees, all-inclusive. Does this align comfortably with the investment bracket you have in mind?"

        # 10. Checkpoint 4: Timeline
        if not self.state["checkpoint_4_timeline"]:
            return "Because this is an expansive thirty-eight acre ecological development with underground utilities and curated parks, we have scheduled phased handovers leading up to full possession in December 2029. Does this horizon match your planning timeline?"

        # 11. Pitch Delivery (Phase 2)
        if not self.state["pitch_delivered"]:
            self.state["pitch_delivered"] = True
            self.state["call_stage"] = "PITCH"
            return "Whispers of the Wind is tucked into an exclusive natural valley flanked by Nandi hills. Over seventy-four percent of the community is preserved as open green spaces with natural streams, eco-parks, and a twenty-thousand square foot clubhouse featuring wellness spas, an infinity pool, and sports courts. It is designed as a pollution-free haven just twenty minutes from the airport."

        # 12. Call to Action (Phase 3)
        if not self.state["cta_proposed"]:
            self.state["cta_proposed"] = True
            self.state["call_stage"] = "CTA"
            return "Given your interest, I would love to arrange a priority walkthrough with our Senior Property Specialist—either over a private video call or hosting you for a private site tour this weekend. Would Saturday morning or Sunday afternoon suit your schedule better?"

        # 13. Closing / Appointment Finalization
        if any(w in t for w in ["saturday", "sunday", "weekend", "morning", "afternoon", "11", "works", "fine", "send on whatsapp"]):
            self.state["appointment_scheduled"] = True
            self.state["call_stage"] = "CLOSED"
            if self.state["language"] == "hinglish":
                return "Zaroor sir! Maine aapka slot book kar liya hai, aur official master layout brochure aur location pin turant aapke WhatsApp par share kar raha hoon. Bohot shukriya aapke waqt ke liye, and have a wonderful day!"
            return "Terrific! I have confirmed your appointment, and I am sending the valley master plan, RERA documents, and location pin to your WhatsApp right now. Thank you so much for your time, and have a wonderful day ahead!"

        return "Thank you so much! I will WhatsApp you the complete digital walkthrough and master plan right away. Have a wonderful day ahead!"
