export type ChatRole = 'user' | 'assistant' | 'system';

export type SupportedBlockType = 'markdown'; // пока хватит одного

export interface MarkdownBlock {
    id: string;
    type: 'markdown';
    text: string;
}

export type ContentBlock = MarkdownBlock;

export interface ChatMessage {
    id: string;
    role: ChatRole;
    createdAt: number;
    schemaVersion: '2025-01';
    blocks: ContentBlock[];
    meta?: Record<string, unknown>;
}
