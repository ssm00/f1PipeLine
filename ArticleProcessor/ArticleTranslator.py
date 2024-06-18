import openai
import json
import os

with open('key.json', 'r') as file:
    data = json.load(file)
with open('prompt.json', encoding="utf-8") as file:
    promt_json = json.load(file)
prompt = promt_json['prompt']
key = data['api_key']

client = openai.OpenAI(api_key=key)


completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": """
McLaren have agreed a fresh multi-year contract extension with Oscar Piastri that will keep the Australian at the British team until at least the end of 2026.

Piastri already had a deal to race for the team in 2024, having signed a multi-year agreement to make his debut this season, but so strong have his performances been so far in 2023, McLaren wanted to cement his long-term future.

OSCAR’S AWARDS: The stunning stats behind Piastri’s stellar junior career

The 22-year-old took his first top-three finish in F1 when he secured second in the Sprint in Belgium and has scored points on six occasions, most recently in Singapore when he fought back from 17th to finish seventh.

“It’s fantastic to confirm that Oscar has signed a multi-year extension with the team,” said Team Principal Andrea Stella. “Oscar is an asset to McLaren and constantly impresses with his performance, work ethic and attitude, so it was an easy decision for the team to make.

“He has already proved pivotal to the team, so it’s brilliant to have his vote of confidence as we push to win championships again in the future. I look forward to seeing him develop with us as we continue this journey together.”

piastri-spa-sprint-2023.png
Piastri qualified and finished second during the Sprint action at Spa-Francorchamps

McLaren CEO Zak Brown added: “I’m delighted to be continuing our partnership with Oscar through to the end of 2026. He’s an incredible talent and an asset to the team so it’s fantastic to be committing to each other in the long term.

“Oscar is already proving what he can do out on track and has been instrumental in the turn around we’ve had so far this season. He’s fit into the team brilliantly and is really valued by the whole McLaren Racing family. I’m excited to see how he continues to grow both on and off track.”

READ MORE: ‘We’re all very proud of him’ – Webber heaps praise on Piastri for ‘phenomenal’ first half of rookie F1 season

Piastri said: “I am thrilled to be extending my partnership with McLaren for many years. I want to be fighting it out at the front of the grid with this team and I am excited by the vision and foundations that are already being laid to get us there.

“The welcome that I have received and the relationships that I have built make this feel like home already. The team’s consistent commitment in me has made me feel incredibly valued and the desire from the team for me to be part of its long-term future made this an easy decision.

Play Video
All Access: McLaren HQ Tour with Oscar Piastri

“To be wanted like that and for the team to show so much belief in me after just half a season, means a lot.

“Stability is a huge advantage in this early part of my career and to have that with a brand as prestigious as McLaren gives me the opportunity to continue the work that we’ve started.

READ MORE: Piastri reacts to his mum becoming a social media sensation amid F1 success

“We’ve enjoyed some good moments together in my rookie season, but I’m excited to work together with everyone at MTC over the coming years to create some great moments.”

Piastri will continue racing alongside Lando Norris, who has finished second three times in 2023, with the Briton’s McLaren deal running until at least the end of 2025.
"""}
  ]
)

print(completion.choices[0].message.content)
