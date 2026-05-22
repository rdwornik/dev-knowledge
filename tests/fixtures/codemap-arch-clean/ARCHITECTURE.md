# Architecture

<!-- CODEMAP:START -->
flowchart TD
    pkg_a[pkg_a]
    pkg_b[pkg_b]
    pkg_a --> pkg_b
    classDef foundation fill:#e8e8e8,stroke:#888
    classDef core fill:#bde0fe,stroke:#1971c2
    classDef orchestration fill:#a5d8ff,stroke:#1971c2
    classDef interface fill:#74c0fc,stroke:#1864ab
    classDef orphan fill:#fff5f5,stroke:#fa5252,stroke-dasharray:4 4
    classDef cycle stroke:#e03131,stroke-width:2px
    click pkg_a href "src/pkg_a/" "Open pkg_a"
    click pkg_b href "src/pkg_b/" "Open pkg_b"
<!-- CODEMAP:END -->
