"""Tone/style profiles for content generation."""


TONES = {
    "edukatif": {
        "name": "Edukatif",
        "description": "Penjelasan jelas, step-by-step, mudah dipahami pemula",
        "style": "Jelaskan konsep dengan bahasa sederhana. Gunakan analogi. Buat poin-poin yang actionable. Ajak audience mempraktikkan.",
        "pembuka": [
            "Sering bingung soal...?",
            "Banyak orang salah paham soal...",
            "Tahu gak sih, kenapa kebanyakan orang gagal manifestasi?",
            "Hari ini kita bahas...",
            "Ini yang perlu kamu pahami:",
        ],
        "penutup": [
            "Save post ini untuk referensi!",
            "Coba praktekan hari ini dan rasakan bedanya.",
            "Follow untuk materi LOAS selanjutnya!",
            "Bagikan ke teman yang lagi belajar manifestasi!",
            "Kalo ada pertanyaan, komen di bawah ya!",
        ],
        "emoji_style": "minimal",
    },
    "motivational": {
        "name": "Motivational",
        "description": "Semangat, powerful, bikin gerak",
        "style": "Gunakan short sentences yang impactful. Power words. Ajak action. Inspirasi dari Neville.",
        "pembuka": [
            "Ini bukan sekadar teori.",
            "Waktunya kamu bangun dari ilusi.",
            "Stop. Baca ini.",
            "Kamu lebih kuat dari yang kamu kira.",
            "Hari ini adalah hari perubahan.",
        ],
        "penutup": [
            "Share ke story kamu dan tag @nevgoinstitute!",
            "Save ini — kamu butuh reminder ini besok.",
            "DM 'LOAS' untuk deep dive!",
            "Follow sekarang sebelum terlambat!",
            "Komen 'SETUJU' jika kamu bicara!",
        ],
        "emoji_style": "moderate",
    },
    "conversational": {
        "name": "Conversational",
        "description": "Casual, teman ngobrol, relatable",
        "style": "Seperti ngobrol dengan teman. Gunakan 'kamu', 'gue', bahasa santai tapi tetap berbobot. Ajak diskusi.",
        "pembuka": [
            "Jujur aja sama kamu...",
            "Pernah nggak sih rasain gini...",
            "Kata siapa manifestasi itu ribet?",
            "Gue mau jujur sama kamu soal ini...",
            "Yang sering gue denger di grup...",
        ],
        "penutup": [
            "Setuju gak? Komen di bawah!",
            "Ada yang pernah ngalamin? Share di komen!",
            "Save buat baca lagi pas butuh!",
            "Follow @nevgoinstitute untuk lebih banyak konten kayak gini! ",
            "Tag teman yang ini buat dia!",
        ],
        "emoji_style": "heavy",
    },
    "authority": {
        "name": "Authority",
        "description": "Percaya diri, expertise, tegas",
        "style": "Langsung ke inti. Tanpa basa-basi. Buktikan dengan logika dan kutipan Neville. Tunjukkan otoritas.",
        "pembuka": [
            "Fakta yang jarang orang bilang:",
            "Ini kesalahan fatal 90% praktisi manifestasi:",
            "Mau manifestasi berhasil? Ini syaratnya.",
            "Most get this wrong. Neville said...",
            "Bukan opini. Ini hukum kesadaran:",
        ],
        "penutup": [
            "Follow untuk ilmu consciousness yang pure.",
            "Konsultasi 1-on-1 — cek link bio.",
            "Save — ini adalah game changer.",
            "Implementasi ini di Private 101. DM untuk daftar.",
            "Follow @nevgoinstitute untuk deep teaching gratis.",
        ],
        "emoji_style": "minimal",
    },
    "soft_sell": {
        "name": "Soft Sell",
        "description": "Gentle promotion, undetectable sales",
        "style": "Educate dulu, promote di ajar tanpa hard sell. Ajak konsultasi. Fokus ke value sebelum CTA.",
        "pembuka": [
            "Sudah coba cara ini?",
            "Banyak yang udah berhasil pakai pendekatan ini.",
            "Ini cara yang jarang diajarkan di tempat lain.",
            "Pengalaman nyata dari komunitas kita?",
            "Yang gue temukan setelah tahunan ngajar...",
        ],
        "penutup": [
            "Mau deep dive lebih? Cek link bio.",
            "Ada kelas intensif setiap bulan. Info lengkap di bio.",
            "Free consultation — DM aja.",
            "Save dan share — bisa bantu teman kalian!",
            "Untuk breakdown lebih detail, follow terus update kita!",
        ],
        "emoji_style": "moderate",
    },
}

HOOKS = {
    "law-of-assumption": [
        "Hukum Asumsi bukan sekadar 'positive thinking'",
        "Kenapa kamu baca ini adalah jawaban doamu",
        "Ada hukum yang bekerja di balik semua manifestasi",
        "Inilah hukum paling powerful yang pernah Neville ajarkan",
    ],
    "sats": [
        "30 menit sebelum tidur adalah waktu paling powerful",
        "Teknik yang dipakai Neville untuk manifestasi kilat",
        "Begitu simple tapi dipahami orang",
        "Ini cara yang Neville sendiri praktekan setiap malam",
    ],
    "identity": [
        "Masalahnya bukan teknik manifestasimu",
        "Salah satu konsep paling keliru dalam LOAS",
        "Siapa kamu sekarang = realitimu besok",
        "kebanyakan fokus ke teknik, bukan ke ini",
    ],
    "money": [
        "Uang datang kepada kesadaran yang match dengannya",
        "Bukan soal kerja keras. Tapi soal identify",
        "Kesalahpahaman terbesar soal kekayaan",
        "Debt bukan masalah fisik - tapi masalah kesadaran",
    ],
    "love": [
        "Jangan mencari pasangan - JADILAH pasangan yang kamu inginkan",
        "Yang kamu tarik = yang kamu conceive",
        "Cinta bukan untuk dicari, tapi untuk dijadi",
        "Relationship problems? Check your self-concept",
    ],
    "mistakes": [
        "Kesalahan #3 adalah yang paling sering dilakukan",
        "Banyak yang udah belajar bertahun-tahun tapi gagal karena ini",
        "Penyebaban manifestasi yang kebalik",
        "Kebanyakan gagal di tahap ini tanpa sadar",
    ],
}

CTA_TEMPLATES = [
    "Save post ini untuk referensi! ",
    "Follow @nevgoinstitute untuk materi LOAS lebih dalam! ",
    "Komen 'LOAS' kalo mau DM materi gratis! ",
    "Share ke story kamu dan tag @nevgoinstitute! ",
    "Tag teman yang lagi belajar manifestasi! ",
    "DM 'PRIVATE' untuk konsultasi gratis! ",
    "Cek link bio untuk kelas lebih dalam! ",
    "Save dan besok pagi baca lagi! ",
    "Puji Tuhan atas insight ini? Komen 'AMIN'! ",
    "Mau master konsep ini? Link di bio! ",
]


HASHTAG_SETS = [
    ["#lawofassumption", "#nevillegoddard", "#manifestasi", "#lawfattraction", "#lawofassumtioncoach", "#consciousmanifestation", "#nevillegoddardteaching", "#mindsetshift", "#identityshift", "#spiritualawakening"],
    ["#lawofassumption", "#motivasi", "#manifesting101", "#loa", "#manifestyourlife", "#spiritualgrowth", "#innerwork", "#lawofattraction", "#nevillegoddard", "#consciouscreation"],
    ["#lawofassumption", "#lawofattraction", "#nevillegoddard", "#manifestasi", "#lawofassumtion", "#identityshift", "#consciousness", "#spirituallife", "#selfdevelopment", "#beginswithin"],
    ["#lawofassumption", "#spiritualawakening", "#manifesting", "#nevillegoddardwisdom", "#imaginationcreatesreality", "#stateofconsciousness", "#innerpower", "#lawofattraction", "#dreambelieveachieve", "#neville"],
    ["#lawofassumption", "#nevillegoddard", "#lawofattraction", "#manifestasi", "#mindset", "#spiritualgrowth", "#selfawareness", "#identity", "#consciousness", "#lawofassumtioncoach"],
    ["#lawofassumption", "#nevillegoddard", "#lawofattraction", "#manifesting", "#spirituallife", "#visualization", "#faith", "#karma", "#innerpeace", "#purpose"],
]


def apply_tone(text, tone_name="edukatif"):
    """Apply tone characteristics to text."""
    tone = TONES.get(tone_name, TONES["edukatif"])
    return {"text": text, "tone": tone_name, "style": tone["style"]}


def get_hook(topic):
    """Get a random hook for a topic."""
    topic_lower = topic.lower().replace(" ", "-")
    for key, hooks in HOOKS.items():
        if key in topic_lower or topic_lower in key:
            import random
            return random.choice(hooks)
    import random
    return random.choice([
        "Ini adalah inti yang sering terlewat:",
        "Perlu kamu pelajari:",
        "Jangan skip ini:",
        "Inilah rahasiam yang jarang dibicarakan:",
    ])


def get_hashtag_set(index=None):
    """Get a rotating hashtag set."""
    import random
    if index is not None:
        return HASHTAG_SETS[index % len(HASHTAG_SETS)]
    return random.choice(HASHTAG_SETS)
