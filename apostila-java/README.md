# 🚀 Apostila Java + Spring + Hexagonal Architecture

Apostila interativa em HTML para o plano intensivo de 2 semanas de Java + Spring Boot + Arquitetura Hexagonal.

## 📋 Características

- ✅ Interface moderna e responsiva
- ✅ 14 aulas completas com conteúdo detalhado
- ✅ Exemplos de código práticos
- ✅ Mini-desafios em cada aula
- ✅ Links para recursos externos
- ✅ Navegação entre aulas
- ✅ Design responsivo para mobile
- ✅ **Gerador de projetos Java/Maven**

## 🚀 Como usar

### 1. Acessar a Apostila

1. Abra o arquivo `index.html` no seu navegador
2. Navegue pelo menu para acessar as aulas
3. Cada aula tem navegação para próxima/anterior

### 2. Criar Projetos Java

Use o script para criar projetos Java rapidamente:

```bash
# Dar permissão (apenas uma vez)
chmod +x create-java-project.sh

# Criar novo projeto
./create-java-project.sh meu-projeto

# Entrar no projeto
cd meu-projeto

# Compilar e testar
mvn clean compile
mvn test
```

📖 **Veja [PROJETO_BASE.md](PROJETO_BASE.md) para mais detalhes**

## 📁 Estrutura

```
apostila-java/
├── index.html                    # Página principal com menu
├── aula-01.html até aula-14.html # Aulas completas
├── styles.css                    # Estilos compartilhados
├── create-java-project.sh        # Script gerador de projetos
├── template-pom-spring.xml       # Template pom.xml para Spring Boot
├── template-pom-jpa.xml          # Template pom.xml para Spring Boot + JPA
├── PROJETO_BASE.md              # Guia de uso do gerador
└── README.md                     # Este arquivo
```

## 🎯 Conteúdo

A apostila contém:

- **Semana 1**: Java + Spring Boot Base (7 dias)
  - Setup, OOP, Spring Boot, JPA, Testes, DTOs, Docker
- **Semana 2**: Arquitetura Hexagonal e Boas Práticas (7 dias)
  - Hexagonal Architecture, Ports/Adapters, Segurança, Projeto Final

## 🛠️ Templates de Projeto

### Para Aulas 01-02 (Java Puro)
```bash
./create-java-project.sh aula01-exercicios
```

### Para Aula 03+ (Spring Boot)
```bash
./create-java-project.sh spring-boot-api
# Depois substitua o pom.xml pelo template-pom-spring.xml
```

### Para Aula 04+ (Spring Boot + JPA)
```bash
./create-java-project.sh jpa-api
# Depois substitua o pom.xml pelo template-pom-jpa.xml
```

## 💡 Dicas de Uso

1. **Um projeto por aula**: Crie projetos separados para praticar cada conceito
2. **Projeto final**: Use um projeto único para o projeto final (Aula 14)
3. **Versionamento**: Use Git para versionar seus projetos
4. **IntelliJ IDEA**: Importe como projeto Maven existente

## 📝 Notas

- Todos os links para vídeos do YouTube são pesquisas genéricas
- Você pode atualizar os links com URLs específicas se preferir
- A apostila funciona offline após o primeiro carregamento
- Os projetos gerados são compatíveis com Java 17 e Maven

---

**Bons estudos! 🚀**


