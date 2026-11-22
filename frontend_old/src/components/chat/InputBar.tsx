import { forwardRef } from 'react';
import { faPaperPlane } from '@fortawesome/free-regular-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

interface InputBarProps {
    val: string;
    handleChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
    onSend: () => void;
    disabled?: boolean;
}

const InputBar = forwardRef<HTMLTextAreaElement, InputBarProps>(
    ({ val, handleChange, onSend, disabled }, ref) => {
        const handleSubmit = (e: React.FormEvent) => {
            e.preventDefault();
            if (disabled) return;
            onSend();
        };
        return (
            <div className="w-2/3">
                <form onSubmit={handleSubmit}>
                    <div className="flex border-2  rounded-4xl items-center overflow-hidden">
                        <div className="w-full h-full mx-2 p-4 flex items-center">
                            <textarea
                                placeholder="Write message..."
                                name="promt-textarea"
                                id="promt-textarea"
                                maxLength={10000}
                                rows={1}
                                wrap="soft"
                                value={val}
                                onChange={handleChange}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && !e.shiftKey) {
                                        e.preventDefault();      // so that a new line is not added
                                        if (!disabled) onSend(); // send message
                                    }
                                }}
                                ref={ref}
                                className="w-full px-2 border-none outline-none leading-[1.1rem] max-h-[calc(10*1.1rem)] overflow-y-auto focus:outline-none focus:ring-0 resize-none scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200"
                            ></textarea>
                        </div>
                        <button
                            type="submit"
                            className={`flex items-center justify-center rounded-full w-10 h-10 mr-2 flex-none shrink-0 min-w-10 transition-all 
                                ${
                                    disabled
                                        ? 'bg-gray-200 opacity-50'
                                        : 'bg-gray-300 hover:scale-105 hover:cursor-pointer'
                                }`}
                        >
                            <FontAwesomeIcon
                                icon={faPaperPlane}
                                onClick={!disabled ? onSend : undefined}
                                className="flex align-middle"
                            />
                        </button>
                    </div>
                </form>
            </div>
        );
    }
);

export default InputBar;
