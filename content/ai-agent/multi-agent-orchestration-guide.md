---
title: "Guide: Multi-Agent Orchestration untuk Complex Tasks"
date: 2026-03-22
draft: false
slug: "multi-agent-orchestration-guide"
description: "Cara setup multiple AI agents yang bekerja sama menyelesaikan task kompleks. Lengkap dengan kode Python dan arsitektur desain."
categories: [Ai Agent]
tags: ['multi-agent', 'orchestration', 'advanced', 'python', 'crewai', 'autogen']
ShowShareLinks: true
ShowReadingTime: true
ShowToc: true
---

Jadi ceritanya, bulan lalu aku dapat project freelance yang bikin pusing. Klien minta bikin sistem yang bisa riset topik, nulis draft artikel, review hasilnya, dan publish ke WordPress — semua otomatis. Satu AI agent? Gak cukup. Butuh beberapa agent yang masing-masing punya peran spesifik.

Dan ternyata, itu namanya multi-agent orchestration. Di guide ini, aku bakal share cara build sistem kayak gitu dari nol.

## Kenapa Gak Cukup Pakai Satu Agent?

Bayangin kamu punya satu orang yang harus jadi researcher, writer, editor, sekaligus publisher sekaligus. Hasilnya? Berantakan. Begitu juga sama AI.

Satu agent yang nanggung semua biasanya:
- **Prompt-nya kepanjangan** — context window habis buat instruksi doang
- **Output gak konsisten** — terlalu banyak tugas, fokus pecah
- **Sulit debug** — gak tau bagian mana yang fail

Dengan multi-agent, masing-masing punya role spesifik. Komunikasi antar agent di-orchestrate oleh satu coordinator. Hasilnya jauh lebih rapi.

## Arsitektur Multi-Agent

Ada beberapa pola yang umum dipakai:

**1. Sequential (Pipeline)**
Agent A → Agent B → Agent C → Output

Cocok untuk workflow yang linear. Contoh: riset → tulis → review.

**2. Hierarchical (Supervisor)**
Supervisor membagi task ke worker agents, terus compile hasilnya.

Cocok untuk task yang bisa dipecah jadi sub-tasks paralel.

**3. Debate / Discussion**
Beberapa agent berdiskusi sampai mencapai konsensus.

Cocok untuk decision-making yang butuh multiple perspectives.

Aku bakal fokus ke pattern pertama dan kedua karena paling sering dipakai di production.

## Prerequisites

Sebelum mulai, siapkan ini:

- Python 3.10+
- OpenAI API key (atau LLM lain)
- Basic understanding tentang LLM dan prompt engineering

Install dependencies:

```bash
pip install crewai crewai-tools langchain-openai python-dotenv
```

## Cara 1: Manual Orchestration dengan Python

Ini cara paling basic — kita sendiri yang nge-orchestrate antar agent. Gak pakai framework khusus.

```python
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI()

class Agent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.memory = []

    def run(self, task: str, context: str = "") -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]

        if context:
            messages.append({
                "role": "system",
                "content": f"Context from previous steps:\n{context}"
            })

        messages.append({"role": "user", "content": task})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )

        result = response.choices[0].message.content
        self.memory.append({"task": task, "result": result})
        return result


# Define agents
researcher = Agent(
    name="Researcher",
    role="research",
    system_prompt="""Kamu adalah researcher yang jago.
    Tugasmu: cari fakta, data, dan argumen yang relevan.
    Output: bullet points yang terstruktur."""
)

writer = Agent(
    name="Writer",
    role="writing",
    system_prompt="""Kamu adalah content writer yang engaging.
    Tulis dengan gaya casual tapi informatif.
    Pakai data dari researcher sebagai fondasi."""
)

editor = Agent(
    name="Editor",
    role="review",
    system_prompt="""Kamu adalah editor yang kritis.
    Review tulisan, kasih feedback soal:
    - Struktur
    - Kejelasan
    - Fakta yang kurang tepat
    - Grammar
    Output: versi yang sudah di-edit atau feedback."""
)


def orchestrate(topic: str):
    """Sequential orchestration: research → write → edit"""

    # Step 1: Research
    print("🔍 Researching...")
    research_result = researcher.run(
        f"Riset topik: {topic}. Kasih fakta, data, dan angle yang menarik."
    )

    # Step 2: Write
    print("✍️ Writing draft...")
    draft = writer.run(
        f"Tulis artikel tentang: {topic}",
        context=research_result
    )

    # Step 3: Edit
    print("📝 Editing...")
    final = editor.run(
        f"Review dan edit artikel ini:\n\n{draft}",
        context=f"Research data:\n{research_result}"
    )

    return final


# Jalankan
result = orchestrate("Masa depan AI agent di Indonesia 2025")
print(result)
```

Ini works, tapi ada masalah: makin banyak agent, makin ribet nge-manage komunikasinya. Makanya kita butuh framework.

## Cara 2: Pakai CrewAI

CrewAI bikin multi-agent orchestration jadi jauh lebih clean. Konsepnya: kamu define agents dengan role, tasks, dan crew (tim).

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Tools (opsional — agent bisa pakai tools external)
search_tool = SerperDevTool()

# Define Agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Temukan data dan insights terbaru tentang topik yang diminta",
    backstory="""Kamu adalah researcher berpengalaman 10 tahun.
    Kamu jago menemukan data tersembunyi dan menghubungkan dots
    yang orang lain gak lihat.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm="gpt-4"
)

writer = Agent(
    role="Content Writer",
    goal="Tulis artikel yang engaging dan informatif",
    backstory="""Kamu adalah tech writer yang udah publish 500+ artikel.
    Gaya tulisanmu casual tapi authoritative. Pembaca merasa
    kayak ngobrol sama temen yang jago.""",
    verbose=True,
    allow_delegation=False,
    llm="gpt-4"
)

editor = Agent(
    role="Chief Editor",
    goal="Pastikan artikel berkualitas tinggi sebelum publish",
    backstory="""Kamu editor perfeksionis. Kamu cek setiap fakta,
    pastikan flow artikel enak dibaca, dan hapus bagian yang
    gak perlu.""",
    verbose=True,
    allow_delegation=False,
    llm="gpt-4"
)

# Define Tasks
research_task = Task(
    description="""Riset tentang: Multi-Agent AI di Indonesia.
    Cari: use cases lokal, startup yang pakai, data adoption rate,
    challenges yang dihadapi.""",
    expected_output="""Laporan riset dengan:
    - 5 use cases dengan contoh konkret
    - Data statistik terbaru
    - Quotes dari expert""",
    agent=researcher
)

writing_task = Task(
    description="""Berdasarkan hasil riset, tulis artikel blog
    1500-2000 kata. Gaya casual Indonesia, pakai 'aku/kamu'.
    Include code examples kalau relevan.""",
    expected_output="Artikel lengkap siap publish dengan markdown formatting",
    agent=writer,
    context=[research_task]  # Hasil riset jadi input
)

editing_task = Task(
    description="""Review dan edit artikel dari writer.
    Fix grammar, improve flow, verify facts.
    Kasih final version yang siap publish.""",
    expected_output="Artikel final yang sudah di-edit dan siap publish",
    agent=editor,
    context=[writing_task]
)

# Create Crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,  # A → B → C
    verbose=True
)

# Run!
result = crew.kickoff()
print(result)
```

CrewAI bikin setiap agent punya konteks dari task sebelumnya secara otomatis. Kamu tinggal define flow-nya aja.

## Cara 3: Hierarchical dengan AutoGen

Kalau kamu butuh pattern supervisor-worker, Microsoft AutoGen lebih cocok:

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

config = {"model": "gpt-4", "api_key": "your-key"}

# Create agents
planner = AssistantAgent(
    name="Planner",
    system_message="""Kamu adalah project planner.
    Pecah task besar jadi sub-tasks yang manageable.
    Delegasikan ke specialist yang tepat.""",
    llm_config=config
)

coder = AssistantAgent(
    name="Coder",
    system_message="""Kamu adalah senior developer.
    Tulis clean code yang production-ready.
    Selalu include error handling.""",
    llm_config=config
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="""Kamu adalah code reviewer.
    Review code dari Coder. Flag bugs, security issues,
    dan suggest improvements.""",
    llm_config=config
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "output"}
)

# Group chat — agents berdiskusi
groupchat = GroupChat(
    agents=[user_proxy, planner, coder, reviewer],
    messages=[],
    max_round=20
)

manager = GroupChatManager(groupchat=groupchat, llm_config=config)

# Start conversation
user_proxy.initiate_chat(
    manager,
    message="""Buatkan Python script untuk:
    1. Scrape harga emas dari beberapa sumber
    2. Simpan ke database SQLite
    3. Generate grafik tren harga"""
)
```

Di pattern ini, Planner nge-break task, Coder nulis code, Reviewer nge-check. Mereka "berdiskusi" sampai solusinya matang.

## Tips yang Aku Pelajari dari Production

Setelah deploy beberapa multi-agent system, ini lessons yang aku dapet:

**1. Jangan terlalu banyak agent**
3-5 agent itu sweet spot. Lebih dari itu, komunikasi overhead-nya gede banget dan cost API naik drastis.

**2. System prompt harus spesifik**
Jangan kasih instruksi vague. Masing-masing agent harus tau persis:
- Apa role-nya
- Apa yang di-expect sebagai output
- Apa yang BUKAN tanggung jawabnya

**3. Handle failures gracefully**
Agent bisa hallucinate, timeout, atau loop. Selalu kasih:
- Max retry limit
- Timeout per step
- Fallback output

```python
import asyncio

async def safe_agent_run(agent, task, max_retries=3, timeout=60):
    for attempt in range(max_retries):
        try:
            result = await asyncio.wait_for(
                agent.run(task),
                timeout=timeout
            )
            if result and len(result.strip()) > 50:  # Sanity check
                return result
        except asyncio.TimeoutError:
            print(f"Agent {agent.name} timeout (attempt {attempt + 1})")
        except Exception as e:
            print(f"Agent {agent.name} error: {e}")

    return f"[Fallback] Agent {agent.name} gagal setelah {max_retries} attempts"
```

**4. Log everything**
Multi-agent system susah di-debug kalau gak ada logging. Log setiap input/output antar agent.

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

def logged_run(agent, task, context=""):
    logger.info(f">>> {agent.name} receiving task: {task[:100]}...")
    result = agent.run(task, context)
    logger.info(f"<<< {agent.name} output: {result[:200]}...")
    return result
```

**5. Monitor cost**
Multi-agent berarti multiple LLM calls. Satu task bisa 5-10x lebih mahal dari single agent. Selalu track token usage.

## Pola Lanjutan: Agent Communication Protocol

Buat sistem yang lebih robust, kamu bisa bikin protocol komunikasi antar agent:

```python
from pydantic import BaseModel
from enum import Enum
from typing import Optional

class MessageType(str, Enum):
    TASK = "task"
    RESULT = "result"
    QUESTION = "question"
    FEEDBACK = "feedback"

class AgentMessage(BaseModel):
    sender: str
    receiver: str
    message_type: MessageType
    content: str
    metadata: Optional[dict] = None
    priority: int = 1  # 1=low, 5=high

class MessageBus:
    def __init__(self):
        self.messages: list[AgentMessage] = []
        self.agents: dict[str, Agent] = {}

    def register(self, agent: Agent):
        self.agents[agent.name] = agent

    def send(self, message: AgentMessage):
        self.messages.append(message)
        # Dispatch ke receiver
        receiver = self.agents.get(message.receiver)
        if receiver:
            return receiver.run(message.content)
        return None

    def get_history(self, agent_name: str) -> list[AgentMessage]:
        return [
            m for m in self.messages
            if m.sender == agent_name or m.receiver == agent_name
        ]
```

## Kapan Harus Pakai Multi-Agent?

Gak semua project butuh multi-agent. Pakai kalau:

- Task-nya kompleks dan bisa dipecah jadi sub-tasks
- Butuh berbagai expertise (coding + writing + research)
- Quality control penting (ada review step)
- Output panjang yang gak muat di satu context window

Gak perlu kalau:
- Task-nya simple dan linear
- Cuma butuh satu jenis expertise
- Budget API terbatas
- Latency jadi concern (multi-agent = lebih lama)

## Conclusion

Multi-agent orchestration itu powerful tapi bukan silver bullet. Mulai dari yang simple (sequential pattern), terus evolve ke lebih kompleks kalau memang butuh.

Paling penting: test thoroughly sebelum deploy production. Multi-agent system itu unpredictable — yang di dev environment bisa beda banget sama yang di production.

Mau diskusi soal multi-agent architecture? Chat aku di [kontak@dovi.my.id](mailto:kontak@dovi.my.id)!

**Artikel selanjutnya:** [RAG 101: Build AI yang Bisa Akses Database](/ai-agent/rag-retrieval-augmented-generation/) — partner yang pas buat multi-agent system kamu.
