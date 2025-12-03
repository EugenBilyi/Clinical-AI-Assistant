// src/app/components/chat/RenderContent.tsx
import React from 'react';
import { ContentBlock } from '@/lib/types';

interface RenderContentProps {
    content: ContentBlock[];
    isStreaming?: boolean;
    onCopy?: (text: string) => void;
    onExpandBlock?: (blockId: string) => void;
    className?: string;
}

// React.FC   --->   functional component, which can accept and process props (properties) and return JSX

const RenderContent: React.FC<RenderContentProps> = ({
    content,
    isStreaming,
    className,
}) => {
    return (
        <div className={className}>
            {content.map((block) => {
                if (block.type === 'markdown') {
                    return (
                        <p key={block.id} className="whitespace-pre-wrap break-words">
                            {block.text}
                        </p>
                    );
                }

                // на будущее: тут будут table/image/chart и т.д.
                return null;
            })}

            {isStreaming && (
                <span className="inline-block ml-1 w-2 h-4 align-baseline rounded-sm animate-pulse bg-gray-700" />
            )}
        </div>
    );
};

export default RenderContent;
