if __name__ == '__main__':
    import uvicorn
    uvicorn.run('finance_service.app:app', debug=True, port=8080)
