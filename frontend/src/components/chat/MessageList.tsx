import React from 'react';
import MessageBubble from './MessageBubble';
import { ChatMessage } from '@/lib/types';

interface MessageListProps {
    messages: ChatMessage[];
}

const MessageList = ({ messages }: MessageListProps) => {
    return (
        <div className="w-full flex flex-col pr-1 pl-1">
            {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
            ))}
        </div>
    );
};

export default MessageList;
