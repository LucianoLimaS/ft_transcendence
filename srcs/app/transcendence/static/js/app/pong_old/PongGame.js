const TABLE_COLOR = 'black';
const LINE_COLOR = 'gray';
const BALL_COLOR = LINE_COLOR;
const PADDLE_COLOR = LINE_COLOR;
const SCORE_COLOR = LINE_COLOR;

export class PongGame {
    constructor(context, canvasWidth, canvasHeight) {
        this.context = context;
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
    }

    clearCanvas() {
        this.context.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
        this.context.fillStyle = TABLE_COLOR
        this.context.fillRect(0, 0, this.canvasWidth, this.canvasHeight);
    }

    drawHorizontalLine(y, thickness) {
        this.context.fillRect(0, y, this.canvasWidth, thickness);
    }

    drawVerticalDashLine(x, thickness) {
        this.context.beginPath();
        this.context.setLineDash([thickness, thickness]);
        this.context.moveTo(x, 0);
        this.context.lineTo(x, this.canvasHeight);
        this.context.lineWidth = thickness;
        this.context.strokeStyle = LINE_COLOR;
        this.context.stroke();
        this.context.setLineDash([]);
    }

    drawTable(thickness) {
        this.context.fillStyle = LINE_COLOR;
        this.drawHorizontalLine(0, thickness);
        this.drawHorizontalLine(this.canvasHeight - thickness, thickness);
        this.drawVerticalDashLine(this.canvasWidth / 2, thickness);
    }

    drawBall(ball) {
        this.context.fillStyle = BALL_COLOR;
        this.context.beginPath();
        this.context.arc(ball.x + ball.size / 2, ball.y + ball.size / 2, ball.size / 2, 0, Math.PI * 2);
        this.context.fill();
    }

    drawPaddle(paddle) {
        this.context.fillStyle = PADDLE_COLOR;
        this.context.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
    }

    drawScore(score) {
        this.context.fillStyle = SCORE_COLOR;
        this.context.font = "42px Monospace";
        this.context.textAlign = "center";

        // Draw left score
        this.context.fillText(score.left, (this.canvasWidth / 2) - 50, 60);

        // Draw right score
        this.context.fillText(score.right, (this.canvasWidth / 2) + 50, 60);
    }

    drawWin(winner) {
        this.context.font = "bold 42px Monospace";
        const message = "Win!"
        if (winner === "left") {
            this.context.fillText(message, (this.canvasWidth / 4), this.canvasHeight/3);
        } else {
            this.context.fillText(message, 3 * (this.canvasWidth / 4), this.canvasHeight/3);
        }
    }

    drawGameState(gameState) {
        this.clearCanvas();
        this.drawTable(gameState.ball.size);
        this.drawBall(gameState.ball);
        this.drawPaddle(gameState.paddle_left);
        this.drawPaddle(gameState.paddle_right);
        this.drawScore(gameState.score);
        if (gameState.winner) {
            this.drawWin(gameState.winner)
        }
    }
}
