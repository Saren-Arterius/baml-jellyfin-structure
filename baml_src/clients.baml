// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> GPT4o {
  provider openai
  options {
    model "gpt-4o"
    api_key env.OPENAI_API_KEY
  }
}

client<llm> GPT4oMini {
  provider openai
  options {
    model "gpt-4o-mini"
    api_key env.OPENAI_API_KEY
  }
}

client<llm> Sonnet {
  provider anthropic
  options {
    model "claude-3-5-sonnet-20240620"
    api_key env.ANTHROPIC_API_KEY
  }
}


client<llm> Haiku {
  provider anthropic
  options {
    model "claude-3-haiku-20240307"
    api_key env.ANTHROPIC_API_KEY
  }
}

client<llm> Fast {
  provider round-robin
  options {
    // This will alternate between the two clients
    strategy [GPT4oMini, Haiku]
  }
}

client<llm> Openai {
  provider fallback
  options {
    // This will try the clients in order until one succeeds
    strategy [GPT4o, GPT4oMini]
  }
}

client<llm> Local {
  provider ollama
  options {
    default_role "user"
    model "mistral-nemo:12b-instruct-2407-q8_0"
    num_ctx 131072
  }
}

client<llm> OpenRouter {
  provider openai-generic
  options {
    api_key env.OPENROUTER_API_KEY
    base_url "https://openrouter.ai/api/v1"
    model openai/gpt-4o-mini
    // model nousresearch/hermes-3-llama-3.1-405b:free
  }
}

