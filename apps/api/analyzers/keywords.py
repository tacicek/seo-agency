import re
from collections import Counter

# Comprehensive multilingual stop words (English, German, French, Italian, Spanish)
STOPWORDS = set("""
    the a an and or for to of in on with is are was were be by as it this that from at your you we they i our their
    der die das den dem des ein eine einer eines einem einen zur zum bei aus nach vor von mit über durch um nicht
    und oder aber auch wenn dann als wie so noch nur schon mehr sehr viel bereits sein seine seine ihr ihre hat haben
    wird werden kann können muss müssen soll sollen will wollen wurde wurden ist sind war waren sein seine
    ich du er sie es wir ihr ihnen sich mich dich uns euch ihm ihn sie ihnen man einer einem einen
    auf an in zu von bei mit nach über unter durch für um gegen ohne bis seit zwischen hinter neben während
    dieser diese dieses jener jene jenes welcher welche welches solcher solche solches aller alle alles
    mein meine meiner meines meinem meinen dein deine deiner deines deinem deinen
    unser unsere unserer unseres unserem unseren euer eure eurer eures eurem euren
    le la les un une des de du à au aux et ou mais donc car ni ne pas plus moins très tout tous toute toutes
    ce cette ces mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs
    je tu il elle nous vous ils elles on me te se lui en y
    être avoir faire dire aller voir venir pouvoir vouloir devoir savoir prendre mettre donner
    il lo la i gli le un uno una dei degli delle di da a in con su per tra fra
    che e o ma anche se non più molto questo quello come quando dove
    io tu lui lei noi voi loro mi ti si ci vi
    essere avere fare dire andare venire potere volere dovere sapere prendere mettere dare
    el la los las un una unos unas de del a al en con por para sobre entre
    que y o pero también si no más muy este esta estos estas ese esa esos esas
    yo tú él ella nosotros vosotros ellos ellas me te se nos os
    ser estar haber tener hacer ir venir poder querer deber saber poner dar
""".split())

def analyze_keywords(text: str, top_n: int = 25) -> dict:
    """
    Analyze text and extract top keywords with frequency and density.
    
    Features:
    - Multilingual stop word filtering (EN, DE, FR, IT, ES)
    - Minimum word length: 3 characters
    - Case-insensitive analysis
    - Percentage density calculation
    
    Args:
        text: Input text to analyze
        top_n: Number of top keywords to return (default: 25)
        
    Returns:
        dict: {
            "total_words": int,
            "top": [{"word": str, "count": int, "percent": float}]
        }
    """
    # Extract words (alphanumeric + umlauts/accents)
    words = re.findall(r"\b[\w\u00C0-\u017F]+\b", text.lower())
    
    # Filter stop words and short words
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    
    total = len(words) or 1
    freq = Counter(words)
    top = freq.most_common(top_n)
    
    density = [
        {
            "word": w, 
            "count": c, 
            "percent": round(c * 100.0 / total, 2)
        } 
        for w, c in top
    ]
    
    return {
        "total_words": total, 
        "top": density
    }
