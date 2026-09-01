import org.jetbrains.changelog.Changelog

fun properties(key: String) = providers.gradleProperty(key)

plugins {
    // No Kotlin plugin and no Java sources: this project is theme resources only.
    id("java")
    // IntelliJ Platform Gradle Plugin -> https://plugins.jetbrains.com/docs/intellij/tools-intellij-platform-gradle-plugin.html
    id("org.jetbrains.intellij.platform") version "2.18.1"
    // Gradle Changelog Plugin -> https://github.com/JetBrains/gradle-changelog-plugin
    id("org.jetbrains.changelog") version "2.5.0"
}

group = properties("pluginGroup").get()
version = properties("pluginVersion").get()

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        create(properties("platformType"), properties("platformVersion"))
        pluginVerifier()
        zipSigner()
    }
}

intellijPlatform {
    // A colour theme has no searchable settings to index, and building them
    // starts a full IDE, which is by far the slowest step in the build.
    buildSearchableOptions = false

    pluginConfiguration {
        version = properties("pluginVersion")

        // Extract the <!-- Plugin description --> section from README.md.
        description = providers.provider {
            val start = "<!-- Plugin description -->"
            val end = "<!-- Plugin description end -->"
            val lines = layout.projectDirectory.file("README.md").asFile.readText().lines()
            if (!lines.containsAll(listOf(start, end))) {
                throw GradleException("Plugin description section not found in README.md:\n$start ... $end")
            }
            lines.subList(lines.indexOf(start) + 1, lines.indexOf(end)).joinToString("\n")
        }.map { org.jetbrains.changelog.markdownToHTML(it) }

        changeNotes = properties("pluginVersion").map { pluginVersion ->
            with(changelog) {
                renderItem(
                    (getOrNull(pluginVersion) ?: getUnreleased())
                        .withHeader(false)
                        .withEmptySections(false),
                    Changelog.OutputType.HTML,
                )
            }
        }

        ideaVersion {
            sinceBuild = properties("pluginSinceBuild")
            // No until-build: a theme carries no code bound to a platform API, so
            // it stays compatible with future releases. `provider { null }` is the
            // documented way to leave the attribute out entirely.
            untilBuild = provider { null }
        }
    }

    signing {
        certificateChain = providers.environmentVariable("CERTIFICATE_CHAIN")
        privateKey = providers.environmentVariable("PRIVATE_KEY")
        password = providers.environmentVariable("PRIVATE_KEY_PASSWORD")
    }

    publishing {
        token = providers.environmentVariable("PUBLISH_TOKEN")
        // pluginVersion follows SemVer and supports pre-release labels such as
        // 2.1.7-alpha.3, which publish to a matching release channel.
        channels = properties("pluginVersion")
            .map { listOf(it.substringAfter('-', "").substringBefore('.').ifEmpty { "default" }) }
    }

    pluginVerification {
        ides {
            create(
                properties("pluginVerifierIdeVersions")
                    .map { it.split(',').map(String::trim).filter(String::isNotEmpty) }
            )
        }
    }
}

changelog {
    version = properties("pluginVersion")
    groups.empty()
}

tasks {
    wrapper {
        gradleVersion = properties("gradleVersion").get()
    }
}
