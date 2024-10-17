from scripts.write_emails import create_script_for_row
import pandas as pd
from openai import OpenAI

query = "My name is Daniel Ip, and I am the Head of Growth at a startup company called HostU. HostU is marketplace platform that facilitiates medium term housing agreements between university students. This usually means sublease agreements. This is great for college students who sign full year leases, but go on 3 month internships or 6 month co-ops and need to sublease both their own apartments and sublease another apartment where they can stay. Often these students prefer to keep their exchanges with other university students to avoid scams and only share housing with their peers. HostU is intended to be the platform that facilitates those exchanges. Currently we have been valued at 5 million dollars and are in our second round of fundraising. We have around 2500 users currently and are looking to expand that number. I am currently leading an initiative to size markets, and develop marketing/outreach channels at around 15 target universities where we are seeking to expand our presence. A major part of this initiative is looking for student-run organizations at these universities (like consulting or marketing clubs) and asking if they would be interested in doing a project to help us expand to their school and help more students find subleases. Following this is the Title, and the description of a university organization, as well as the university where it is established. If this organization is a marketing organization of some kind, please write an email script for me to reach out to this club and ask if they are interested in a project to expand our marketing and outreach channels. Mention benefits such as the opportunity to work closely with the top-level executives of a venture backed startup company, and opportunities to generate quantifiable results for our growth department. If this is a consulting organization of some kind, please write an email script for me to reach out to this club and ask if they are interested in a project to help us determine the market size in their region, and a market entry strategy. Mention similar benefits as if it were a marketing club fell free to include some of the statistics I gave at the beginning of this message. Specialize the message to the club based on their description."

client = OpenAI()

df = pd.read_excel('data/school-clubs.xlsx')

df['email_script'] = df.apply(lambda row: create_script_for_row(row, query, client), axis=1)

print(df.to_string())

df.to_excel('data/school-clubs-with-email-scripts.xlsx', index=False)

