class _EventApi {
  static _request(url, method, body = undefined) {
      const backend_url = process.env.BACKEND_API_URL ?? 'http://localhost:8000'
      return fetch(`${backend_url}${url}`, {
          method: method,
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
      })
  }

  static makeTest(gradeId) {
    // テストを作成するためのAPI
    return this._request(`/tests/${gradeId}`, 'GET')
  }

  static getItemInfo(itemUuid) {
    // 次の問題を取得するためのAPI
    return this._request(`/items/${itemUuid}`, 'GET')
  }

  static getItemAnswer(itemUuid) {
    // 現在の問題の答えを取得するためのAPI
    return this._request(`/items/${itemUuid}/answer`, 'GET')
  }

  static sendResponseInfo(itemUuid, answerInfo) {
    // ユーザーの回答を送信するためのAPI
    return this._request(`/items/${itemUuid}/response`, 'POST', answerInfo)
  }

//   static updateAgent(avatarInfo) {
//       // エージェントの情報編集API
//       // avatarInfo: AgentDTOに相当するものを渡す
//       return this._request(`/agents/${avatarInfo.agent_id}`, 'PUT', avatarInfo)
//   }

//   static actAction(agent_id, function_dto) {
//       // Playerが関数を実行するためのAPI
//       return this._request(`/agents/${agent_id}/action`, 'POST', function_dto)
//   }

//   static actGenerateAction(agent_id) {
//       // AIが関数を実行するためのAPI
//       return this._request(`/agents/${agent_id}/action`, 'POST', {"type": "undecided"})
//   }

//   static registerVisibleAgent(avatarTable) {
//       // 席情報を登録するAPI
//       return this._request('/agents/recognition', 'POST', avatarTable)
//   }
}

export const EventApi = _EventApi