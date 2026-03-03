"use client"

import { useState } from 'react';

export default function Home() {
    const [question, setQuestion] = useState<string>('');
    const [answer, setAnswer] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    async function handleSubmit() {
        if (!question.trim()) return;
        setLoading(true);
        try {
            const res = await fetch('/api', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question }),
            });
            setAnswer(await res.text());
        } catch (err) {
            setAnswer('Error: ' + (err instanceof Error ? err.message : String(err)));
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="p-8 font-sans">
            <h1 className="text-3xl font-bold mb-4">
                German text corrector
            </h1>
            <div className="w-full max-w-2xl flex flex-col gap-4">
                <textarea
                    className="w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 resize-y"
                    rows={4}
                    placeholder="Type your question…"
                    value={question}
                    onChange={e => setQuestion(e.target.value)}
                />
                <button
                    className="self-start px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    onClick={handleSubmit}
                    disabled={loading}
                >
                    {loading ? 'Loading…' : 'Submit'}
                </button>
                {answer && (
                    <div className="p-6 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm">
                        <p className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap">
                            {answer}
                        </p>
                    </div>
                )}
            </div>
        </main>
    );
}
