import os


def generate_inspection_pdf(
    inspection,
    answers
):

    html_content = f"""
    <html>
    <head>
        <title>Relatório</title>

        <style>
            body {{
                font-family: Arial;
                padding: 40px;
            }}

            h1 {{
                color: #1f2937;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #ccc;
                padding: 10px;
            }}
        </style>

    </head>

    <body>

        <h1>Relatório de Inspeção</h1>

        <p>
            <strong>ID:</strong>
            {inspection.id}
        </p>

        <p>
            <strong>Status:</strong>
            {inspection.status}
        </p>

        <table>

            <thead>
                <tr>
                    <th>Pergunta</th>
                    <th>Resposta</th>
                    <th>Risco</th>
                </tr>
            </thead>

            <tbody>

    """

    for answer in answers:

        html_content += f"""
            <tr>
                <td>{answer.pergunta}</td>
                <td>{answer.resposta}</td>
                <td>{answer.risco}</td>
            </tr>
        """

    html_content += """

            </tbody>

        </table>

    </body>

    </html>
    """

    os.makedirs("generated_reports", exist_ok=True)

    file_path = f"generated_reports/report_{inspection.id}.html"

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html_content)

    return file_path