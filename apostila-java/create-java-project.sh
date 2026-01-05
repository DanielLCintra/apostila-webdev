#!/bin/bash

# Script para criar projeto Java com Maven
# Uso: ./create-java-project.sh nome-do-projeto

if [ -z "$1" ]; then
    echo "❌ Erro: Você precisa fornecer um nome para o projeto"
    echo "Uso: ./create-java-project.sh nome-do-projeto"
    exit 1
fi

PROJECT_NAME=$1
GROUP_ID="com.exemplo"
ARTIFACT_ID=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
BASE_DIR=$(pwd)

echo "🚀 Criando projeto Java: $ARTIFACT_ID"

# Criar estrutura de diretórios
mkdir -p "$ARTIFACT_ID"/src/main/java/com/exemplo
mkdir -p "$ARTIFACT_ID"/src/main/resources
mkdir -p "$ARTIFACT_ID"/src/test/java/com/exemplo
mkdir -p "$ARTIFACT_ID"/src/test/resources

# Criar pom.xml
cat > "$ARTIFACT_ID/pom.xml" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>$GROUP_ID</groupId>
    <artifactId>$ARTIFACT_ID</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>$PROJECT_NAME</name>
    <description>Projeto Java criado para estudos</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <junit.version>5.10.0</junit.version>
    </properties>

    <dependencies>
        <!-- JUnit 5 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>\${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
        </plugins>
    </build>
</project>
EOF

# Criar classe principal
cat > "$ARTIFACT_ID/src/main/java/com/exemplo/App.java" << 'EOF'
package com.exemplo;

public class App {
    public static void main(String[] args) {
        System.out.println("🚀 Projeto Java iniciado com sucesso!");
        System.out.println("Comece a implementar seus códigos aqui.");
    }
}
EOF

# Criar classe de teste
cat > "$ARTIFACT_ID/src/test/java/com/exemplo/AppTest.java" << 'EOF'
package com.exemplo;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AppTest {
    @Test
    void testApp() {
        assertTrue(true, "Teste inicial funcionando!");
    }
}
EOF

# Criar .gitignore
cat > "$ARTIFACT_ID/.gitignore" << 'EOF'
# Compiled class files
*.class

# Log files
*.log

# Package Files
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# IDE
.idea/
*.iml
*.iws
*.ipr
.vscode/
.classpath
.project
.settings/
bin/

# OS
.DS_Store
Thumbs.db
EOF

# Criar README.md
cat > "$ARTIFACT_ID/README.md" << EOF
# $PROJECT_NAME

Projeto Java criado para estudos do curso Java + Spring + Hexagonal Architecture.

## 📁 Estrutura do Projeto

\`\`\`
$ARTIFACT_ID/
├── src/
│   ├── main/
│   │   ├── java/com/exemplo/    # Código fonte principal
│   │   └── resources/            # Arquivos de configuração
│   └── test/
│       ├── java/com/exemplo/     # Código de testes
│       └── resources/            # Recursos para testes
├── pom.xml                       # Configuração Maven
└── README.md                     # Este arquivo
\`\`\`

## 🚀 Como Executar

### Compilar o projeto
\`\`\`bash
mvn clean compile
\`\`\`

### Executar a aplicação
\`\`\`bash
mvn exec:java -Dexec.mainClass="com.exemplo.App"
\`\`\`

### Executar testes
\`\`\`bash
mvn test
\`\`\`

### Gerar JAR
\`\`\`bash
mvn clean package
\`\`\`

## 📚 Próximos Passos

1. Abra o projeto no IntelliJ IDEA
2. Configure o JDK 17 nas configurações do projeto
3. Comece a implementar os exercícios da Aula 01
4. Use este projeto para praticar todos os conceitos aprendidos

## 🛠️ Comandos Úteis

- \`mvn clean\` - Limpa arquivos compilados
- \`mvn compile\` - Compila o projeto
- \`mvn test\` - Executa testes
- \`mvn package\` - Gera JAR
- \`mvn install\` - Instala no repositório local

Bons estudos! 🚀
EOF

echo "✅ Projeto criado com sucesso!"
echo ""
echo "📁 Diretório: $BASE_DIR/$ARTIFACT_ID"
echo ""
echo "📝 Próximos passos:"
echo "   cd $ARTIFACT_ID"
echo "   mvn clean compile"
echo "   mvn test"
echo ""
echo "💡 Dica: Abra o projeto no IntelliJ IDEA para começar a desenvolver!"

