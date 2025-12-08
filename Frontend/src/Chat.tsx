import { useState, useEffect, useRef } from 'react'
import './Chat.css'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const hasInitialized = useRef(false)  // useRef に変更

  const sendMessage = async (questionText?: string) => {
    const question = questionText || input.trim()
    if (!question) return

    // 初回自動送信でない場合のみユーザーメッセージを表示
    if (!questionText) {
      const userMessage: Message = { role: 'user', content: question }
      setMessages(prev => [...prev, userMessage])
      setInput('')
    }
    
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/slidepack/rag', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })

      const data = await response.json()
      const assistantMessage: Message = { 
        role: 'assistant', 
        content: data.answer || 'エラーが発生しました' 
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = { 
        role: 'assistant', 
        content: '接続エラーが発生しました' 
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  // 初回マウント時に自動でメッセージを送信
  useEffect(() => {
    if (!hasInitialized.current) {
      sendMessage('SlidePackは何ができますか？')
      hasInitialized.current = true
    }
  }, [])  // 依存配列を空にする

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>SlidePack RAG チャットボット</h1>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && !isLoading && (
          <div className="empty-state">
            質問を入力してください
          </div>
        )}
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content loading">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
      </div>

      <div className="chat-input-container">
        <textarea
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="質問を入力してください..."
          rows={1}
          disabled={isLoading}
        />
        <button 
          className="send-button" 
          onClick={() => sendMessage()}
          disabled={isLoading || !input.trim()}
        >
          送信
        </button>
      </div>
    </div>
  )
}

export default Chat