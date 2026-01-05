# 📚 Exemplo de Uso - Criando e Usando Projetos

Este guia mostra exemplos práticos de como usar o gerador de projetos em cada etapa do curso.

## 🎯 Aula 01 - Primeiro Projeto Java

### Criar projeto para exercícios da Aula 01

```bash
# Criar projeto
./create-java-project.sh aula01-exercicios

# Entrar no projeto
cd aula01-exercicios

# Compilar
mvn clean compile

# Executar
mvn exec:java -Dexec.mainClass="com.exemplo.App"

# Executar testes
mvn test
```

### Estrutura criada

```
aula01-exercicios/
├── src/
│   ├── main/java/com/exemplo/
│   │   └── App.java          # Classe principal
│   └── resources/
└── src/test/java/com/exemplo/
    └── AppTest.java          # Teste exemplo
├── pom.xml
└── README.md
```

### Implementar exercício da Aula 01

1. Crie `Usuario.java` em `src/main/java/com/exemplo/`:

```java
package com.exemplo;

public record Usuario(String nome, int idade) {}
```

2. Crie `Main.java`:

```java
package com.exemplo;

import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Usuario> usuarios = List.of(
            new Usuario("João", 25),
            new Usuario("Maria", 18),
            new Usuario("Pedro", 30)
        );
        
        usuarios.stream()
            .filter(u -> u.idade() > 20)
            .map(u -> u.nome().toUpperCase())
            .forEach(System.out::println);
    }
}
```

3. Execute:
```bash
mvn exec:java -Dexec.mainClass="com.exemplo.Main"
```

## 🎯 Aula 03 - Spring Boot

### Criar projeto Spring Boot

```bash
# Criar projeto base
./create-java-project.sh spring-boot-api

# Entrar no projeto
cd spring-boot-api

# Substituir pom.xml pelo template Spring Boot
cp ../template-pom-spring.xml pom.xml

# Ou editar manualmente adicionando dependências Spring Boot
```

### Adicionar dependências Spring Boot no pom.xml

Substitua o conteúdo do `pom.xml` pelo template `template-pom-spring.xml` ou adicione:

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

### Criar estrutura Spring Boot

```bash
# Criar packages
mkdir -p src/main/java/com/exemplo/{controller,service,repository}
```

### Criar primeira API

1. Criar `HelloController.java`:

```java
package com.exemplo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    
    @GetMapping("/hello")
    public String hello() {
        return "Olá, Spring Boot!";
    }
}
```

2. Criar `AplicacaoApplication.java`:

```java
package com.exemplo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AplicacaoApplication {
    public static void main(String[] args) {
        SpringApplication.run(AplicacaoApplication.class, args);
    }
}
```

3. Executar:
```bash
mvn spring-boot:run
```

4. Acessar: `http://localhost:8080/hello`

## 🎯 Aula 04 - Spring Boot + JPA

### Atualizar projeto para JPA

```bash
# Se já tem projeto Spring Boot, apenas atualize o pom.xml
# Ou crie novo projeto
./create-java-project.sh jpa-api
cd jpa-api
cp ../template-pom-jpa.xml pom.xml
```

### Adicionar entidade JPA

1. Criar `Usuario.java`:

```java
package com.exemplo.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "usuarios")
public class Usuario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String nome;
    private String email;
    private LocalDateTime dataCriacao;
    
    // Construtores, getters e setters
}
```

2. Criar `UsuarioRepository.java`:

```java
package com.exemplo.repository;

import com.exemplo.entity.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
}
```

3. Configurar `application.properties`:

```properties
spring.datasource.url=jdbc:h2:mem:testdb
spring.h2.console.enabled=true
spring.jpa.hibernate.ddl-auto=update
```

## 🎯 Aula 08+ - Arquitetura Hexagonal

### Criar projeto com estrutura hexagonal

```bash
./create-java-project.sh tasks-api-hexagonal
cd tasks-api-hexagonal
```

### Criar estrutura de packages

```bash
mkdir -p src/main/java/com/exemplo/{domain,application/{port/{in,out},service},infrastructure/{persistence/{entity,repository,mapper},adapters/in/web}}
```

### Estrutura final

```
tasks-api-hexagonal/
├── src/main/java/com/exemplo/
│   ├── domain/
│   │   └── Task.java
│   ├── application/
│   │   ├── port/
│   │   │   ├── in/
│   │   │   │   └── CreateTaskUseCase.java
│   │   │   └── out/
│   │   │       └── TaskRepositoryPort.java
│   │   └── service/
│   │       └── CreateTaskService.java
│   └── infrastructure/
│       ├── persistence/
│       │   ├── entity/
│       │   │   └── TaskEntity.java
│       │   └── repository/
│       │       └── JpaTaskRepositoryAdapter.java
│       └── adapters/in/web/
│           └── TaskController.java
```

## 💡 Dicas Gerais

### Um projeto por conceito

```bash
# Aula 01
./create-java-project.sh aula01-streams

# Aula 02
./create-java-project.sh aula02-oop

# Aula 03
./create-java-project.sh aula03-spring-boot

# Projeto Final (Aula 14)
./create-java-project.sh tasks-api-final
```

### Versionamento com Git

```bash
# Após criar projeto
cd meu-projeto
git init
git add .
git commit -m "Initial commit - projeto base"
```

### Importar no IntelliJ IDEA

1. File → Open
2. Selecione a pasta do projeto
3. IntelliJ detecta automaticamente como projeto Maven
4. Aguarde o download das dependências

### Comandos Maven Úteis

```bash
# Limpar e compilar
mvn clean compile

# Executar testes
mvn test

# Gerar JAR
mvn clean package

# Executar aplicação Spring Boot
mvn spring-boot:run

# Ver dependências
mvn dependency:tree

# Atualizar dependências
mvn versions:display-dependency-updates
```

## 🐛 Solução de Problemas

### Erro: "mvn: command not found"
```bash
# Verificar instalação
which mvn
mvn -version

# Se não instalado, instale o Maven
```

### Erro de compilação
```bash
# Verificar Java
java -version  # Deve ser 17+

# Limpar e recompilar
mvn clean compile
```

### Dependências não baixam
```bash
# Forçar atualização
mvn clean install -U
```

---

**Use estes exemplos como referência para criar seus próprios projetos! 🚀**

