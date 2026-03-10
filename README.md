# ESPShowRepo Docker part

Ukázkový repozitář pro **interní školení Docker a Docker Compose**.

Projekt ukazuje postupně, jak:

* spustit jednoduchý kontejner
* spojit více kontejnerů pomocí **Docker Compose**
* používat **volumes pro persistentní data**
* propojit služby mezi sebou
* vytvořit **vlastní Docker image**

---

# 🚀 Quick Start

Spuštění příkladů:

```bash
cd basic\ single
docker compose up
```

Poté otevři:

```
http://localhost:8080
```

---

# 📦 Projektová struktura

```
ESPShowRepo
│
├─ basic single
│   └─ docker-compose.yml
│
├─ db and web
│   └─ docker-compose.yml
│
├─ elastic and kibana
│   └─ docker-compose.yml
│
├─ final
│   └─ docker-compose.yml
│
└─ own app
    ├─ app.py
    ├─ Dockerfile
    ├─ docker-compose.yml
    └─ requirements.txt
```

---

# 📚 Postup školení

Repozitář je navržen pro **postupné vysvětlování Docker Compose**.

Doporučené pořadí:

1️⃣ **basic single**
jednoduchý web server nginx

2️⃣ **db and web**
přidání PostgreSQL databáze

3️⃣ **elastic and kibana**
logovací stack

4️⃣ **final**
kompletní multi-container aplikace

5️⃣ **own app**
vytvoření vlastního Docker image

---

# 🐳 Docker Compose architektura

```
          ┌─────────────┐
          │    Browser  │
          └──────┬──────┘
                 │
                 ▼
           ┌──────────┐
           │   Web    │
           │  (nginx) │
           └─────┬────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
   ┌───────────┐   ┌──────────────┐
   │ PostgreSQL│   │ Elasticsearch│
   └───────────┘   └──────┬───────┘
                          ▼
                     ┌────────┐
                     │ Kibana │
                     └────────┘
```

Docker Compose vytvoří **společnou síť**, takže kontejnery komunikují pomocí **názvu služby**.

Například:

```
http://elasticsearch:9200
```

---

# 🔧 Nejdůležitější Docker příkazy

```
docker build
docker run
docker ps
docker compose up
docker compose down
```

---

# ⚠️ Nejčastější chyby

### Použití localhost mezi kontejnery

❌ špatně

```
localhost:5432
```

✅ správně

```
db:5432
```

---

### Zapomenuté volumes

Databáze bez volume **ztratí data při restartu kontejneru**.

---

### Špatné mapování portů

```
HOST_PORT:CONTAINER_PORT
```

například

```
8080:80
```

---

# 📖 Shrnutí

| koncept        | význam                       |
| -------------- | ---------------------------- |
| Docker image   | šablona aplikace             |
| Container      | běžící instance image        |
| Docker Compose | orchestrátor více kontejnerů |
| Dockerfile     | návod jak image vytvořit     |

---

# 🏫 Účel projektu

Repozitář slouží pouze pro **interní školení a demonstraci Docker workflow**.
