# AI Study Hub — ERD

```mermaid
erDiagram
    User ||--|| Profile : has
    User ||--o{ Task : owns
    User ||--o{ Category : owns
    User ||--o{ Tag : owns
    User ||--o{ Note : owns
    User ||--o{ Resource : owns
    User ||--o{ Activity : logs
    User ||--o{ AIConversation : starts
    Category ||--o{ Note : groups
    Note }o--o{ Tag : tagged_with
    ResourceType ||--o{ Resource : classifies
    AIConversation ||--o{ AIMessage : contains
```