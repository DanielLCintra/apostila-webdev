# 📦 Projeto Base Java - Guia de Uso

Este diretório contém um script para criar projetos Java com Maven de forma rápida e padronizada.

## 🚀 Como Usar

### Opção 1: Script Shell (Recomendado)

```bash
# Dar permissão de execução (apenas uma vez)
chmod +x create-java-project.sh

# Criar novo projeto
./create-java-project.sh meu-projeto-java
```

### Opção 2: Executar Diretamente

```bash
bash create-java-project.sh meu-projeto-java
```

## 📋 O que o Script Cria

O script cria uma estrutura completa de projeto Maven com:

- ✅ Estrutura de pastas padrão Maven
- ✅ `pom.xml` configurado com Java 17
- ✅ Classe principal (`App.java`)
- ✅ Classe de teste exemplo (`AppTest.java`)
- ✅ `.gitignore` configurado
- ✅ `README.md` com instruções

## 📁 Estrutura Gerada

```
meu-projeto-java/
├── src/
│   ├── main/
│   │   ├── java/com/exemplo/
│   │   │   └── App.java
│   │   └── resources/
│   └── test/
│       ├── java/com/exemplo/
│       │   └── AppTest.java
│       └── resources/
├── pom.xml
├── .gitignore
└── README.md
```

## 🎯 Exemplos de Uso

### Criar projeto para Aula 01
```bash
./create-java-project.sh aula01-exercicios
cd aula01-exercicios
```

### Criar projeto para Aula 03 (Spring Boot)
```bash
./create-java-project.sh spring-boot-api
cd spring-boot-api
# Depois adicione dependências Spring Boot no pom.xml
```

### Criar projeto final
```bash
./create-java-project.sh tasks-api-final
cd tasks-api-final
```

## 🔧 Personalização

Após criar o projeto, você pode:

1. **Adicionar dependências** - Edite o `pom.xml`
2. **Configurar Spring Boot** - Adicione as dependências necessárias
3. **Criar packages** - Organize seu código em packages
4. **Adicionar recursos** - Coloque arquivos em `src/main/resources`

## 📚 Integração com as Aulas

### Aula 01-02: Java Puro
- Use o projeto base como está
- Implemente classes, records, streams
- Crie testes unitários

### Aula 03+: Spring Boot
- Adicione dependências Spring Boot no `pom.xml`
- Crie estrutura de packages (controller, service, repository)
- Configure `application.properties`

### Aula 08+: Arquitetura Hexagonal
- Organize em packages: domain, application, infrastructure
- Implemente ports e adapters
- Separe domínio de infraestrutura

## 💡 Dicas

- **Um projeto por aula**: Crie um projeto separado para cada aula
- **Projeto final**: Use um projeto único para o projeto final (Aula 14)
- **Versionamento**: Use Git para versionar seus projetos
- **IntelliJ IDEA**: Importe como projeto Maven existente

## 🐛 Solução de Problemas

### Erro: "mvn: command not found"
```bash
# Instale o Maven primeiro
# macOS
brew install maven

# Linux
sudo apt install maven

# Windows
# Baixe de https://maven.apache.org/download.cgi
```

### Erro de permissão no script
```bash
chmod +x create-java-project.sh
```

### Projeto não compila
- Verifique se Java 17 está instalado: `java -version`
- Verifique se Maven está instalado: `mvn -version`
- Limpe e recompile: `mvn clean compile`

## 📖 Recursos Adicionais

- [Documentação Maven](https://maven.apache.org/guides/)
- [Java 17 Documentation](https://docs.oracle.com/en/java/javase/17/)
- [IntelliJ IDEA Guide](https://www.jetbrains.com/help/idea/maven.html)

