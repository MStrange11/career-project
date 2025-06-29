from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash") # gemini-1.5-flash is free to use, but has some limitations
# model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2) # need to add balance (its not free)
try:
    res = model.invoke("Write importance of creativity in childs before teenage life?").content
except Exception as e:
    res = str(e)

print(res)

"""
OUTPUT:

Creativity in children before their teenage years is profoundly important for their overall development and future success.  It's not just about producing pretty artwork; it's a vital skillset that underpins many aspects of their lives. Here's why:

Cognitive Development:

Problem-solving skills: Creative activities encourage children to think outside the box, explore different solutions, and persevere through challenges.  They learn to approach problems from multiple angles, a skill crucial for academic and real-world success.

Critical thinking:  Creativity isn't just about making things; it's about evaluating ideas, making choices, and refining creations. This fosters critical thinking skills essential for analyzing information and making informed decisions.
Improved memory and learning: Engaging in creative activities enhances memory retention and improves learning abilities. The active process of creating and experimenting strengthens neural pathways in the brain.
Enhanced language development: Creative expression, whether through writing, storytelling, or dramatic play, boosts vocabulary, grammar, and communication skills.

Emotional and Social Development:

Self-expression and confidence: Creativity provides a safe outlet for children to express their emotions, thoughts, and ideas. This self-expression fosters self-confidence and a stronger sense of self.
Emotional regulation: Engaging in creative pursuits can help children manage and regulate their emotions.  Art, music, and play can be therapeutic and calming.
Social skills: Collaborative creative activities, such as group projects or theatrical performances, encourage teamwork, cooperation, and communication skills.  Children learn to negotiate, compromise, and appreciate diverse perspectives.
Resilience:  The creative process often involves setbacks and failures.  Learning to overcome these challenges builds resilience and perseverance, crucial for navigating life's difficulties.

Future Success:

Innovation and adaptability: A creative mindset is essential for innovation and adaptability in a rapidly changing world.  Creative individuals are better equipped to solve complex problems and come up with innovative solutions.
Career opportunities: Many professions, from engineering and design to medicine and business, require creativity and innovative thinking.  Cultivating creativity in childhood lays the foundation for a wide range of future career paths.      


In short, nurturing creativity in children before adolescence is an investment in their future. It equips them with essential cognitive, emotional, and social skills that will benefit them throughout their lives.  Providing opportunities for creative expression through play, art, music, storytelling, and other activities is crucial for their healthy development and overall well-being.

"""