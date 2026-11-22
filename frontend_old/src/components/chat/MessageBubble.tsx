import React from 'react';
import { ChatMessage } from '@/lib/types';
import RenderContent from './RenderContent';

interface MessageBubbleProps {
    message: ChatMessage;
    isStreaming?: boolean;
}

const MessageBubble = ({ message, isStreaming }: MessageBubbleProps) => {
    const isUser = message.role === 'user';

    const generalContainer =
        'min-w-0 max-w-[70%] break-all whitespace-pre-wrap overflow-hidden flex p-1 rounded-md';
    const userClass = 'bg-gray-800 max-w-xl text-white border-2 border-black';
    const chatClass = 'bg-gray-100 max-w-5xl text-black border-2 border-gray-300';

    return (
        <div className={`flex pb-3 w-full ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={[generalContainer, isUser ? userClass : chatClass].join(' ')}>
                <RenderContent content={message.blocks} isStreaming={isStreaming} />
            </div>
        </div>
    );
};

export default MessageBubble;
