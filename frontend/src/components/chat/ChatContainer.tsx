'use client';
import { useRef, useState, useEffect } from 'react';
import InputBar from './InputBar';
import MessageList from './MessageList';
import { ChatMessage } from '@/lib/types';
import SystemNote from './SystemNote';
import { faArrowDown } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const ChatContainer = () => {
    const [val, setVal] = useState('');
    const [messages, setMessages] = useState<ChatMessage[]>([]); // Simulation for show text from InputBar
    const textAreaRef = useRef<HTMLTextAreaElement>(null);
    const [isAtBottom, setIsAtBottom] = useState(true);
    const [isThinking, setIsThinking] = useState(false);
    const thinkingPhrases = ['Thinking', 'Thinking.', 'Thinking..', 'Thinking...'];
    const [thinkingIndex, setThinkingIndex] = useState(0);
    const wrapperContainer = useRef<HTMLDivElement | null>(null);
    const [isOverflow, setIsOverflow] = useState(false); // > 520px

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setVal(e.target.value);
    };

    const handleSend = () => {
        const text = val.trim();
        if (!text) return;

        const timestamp = Date.now().toString();

        const userMessage: ChatMessage = {
            id: timestamp,
            role: 'user',
            createdAt: Date.now(),
            schemaVersion: '2025-01',
            blocks: [
                {
                    id: 'b-' + timestamp,
                    type: 'markdown',
                    text,
                },
            ],
        };

        setMessages((prev) => [...prev, userMessage]);
        setVal('');

        // --- optional: fake answer from Assistant. Chat will not be empty
        const assistantMessage: ChatMessage = {
            id: timestamp + '-assistant',
            role: 'assistant',
            createdAt: Date.now(),
            schemaVersion: '2025-01',
            blocks: [
                {
                    id: 'b-a-' + timestamp,
                    type: 'markdown',
                    text: `You said: "${text}"`,
                },
            ],
        };

        setIsThinking(true);

        setTimeout(() => {
            setMessages((prev) => [...prev, assistantMessage]);
            setIsThinking(false);
        }, 1000);
    };

    const handleScroll = () => {
        const el = wrapperContainer.current;
        if (!el) return;

        const distanceFromBottom = el.scrollHeight - (el.scrollTop + el.clientHeight);
        setIsAtBottom(distanceFromBottom < 30);
    };

    const handleScrollDown = () => {
        const el = wrapperContainer.current;
        if (!el) return;

        el.scrollTo({
            top: el.scrollHeight,
            behavior: 'smooth',
        });
    };

    useEffect(() => {
        const el = wrapperContainer.current;
        if (!el) return;

        // console.log('Scroll height = ', el.scrollHeight);
        if (el.scrollHeight > 560) {
            setIsOverflow(true);
        }
    }, [messages]);

    useEffect(() => {
        const el = textAreaRef.current;
        if (!el) return;
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
    }, [val]);

    useEffect(() => {
        if (!isThinking) return;

        const interval = setInterval(() => {
            setThinkingIndex((i) => (i + 1) % thinkingPhrases.length);
        }, 300); // change word time

        return () => clearInterval(interval);
    }, [isThinking]);

    useEffect(() => {
        const el = wrapperContainer.current;
        if (!el) return;
        if (!isAtBottom) return;

        el.scrollTop = el.scrollHeight; // scrollTop - how much it scrolled from up, scrollHeight — full height of content
    }, [messages, isAtBottom]);

    return (
        <div className="relative flex flex-col h-full w-full max-w-6xl mx-auto pt-2">
            <div className="flex-1 overflow-y-auto" ref={wrapperContainer} onScroll={handleScroll}>
                <MessageList messages={messages} />

                {isThinking && (
                    <div className="w-full flex justify-center">
                        <SystemNote text={thinkingPhrases[thinkingIndex]} />
                    </div>
                )}
            </div>

            {isOverflow && !isAtBottom && (
                <div className="flex absolute bottom-18 right-[50%] justify-center pb-3">
                    <button
                        onClick={handleScrollDown}
                        className="bg-white border-2 border-gray-600 flex items-center justify-center rounded-full w-7 h-7 mr-2 
                            hover:scale-105 transition-all hover:cursor-pointer flex-none shrink-0 min-w-7"
                    >
                        <FontAwesomeIcon icon={faArrowDown} className="flex align-middle" />
                    </button>
                </div>
            )}

            <div className="w-full flex justify-center pb-4">
                <InputBar
                    val={val}
                    onSend={handleSend}
                    handleChange={handleChange}
                    ref={textAreaRef}
                    disabled={isThinking}
                />
            </div>
        </div>
    );
};

export default ChatContainer;
