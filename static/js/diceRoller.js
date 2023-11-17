// diceRoller.js

document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll('.navbar a:visited');

    links.forEach(function(link) {
        link.classList.add('visited-link');
    });
});

function openDiceRoller() {
    document.getElementById('diceRollerPopup').style.display = 'block';
}

function closeDiceRoller() {
    document.getElementById('diceRollerPopup').style.display = 'none';
}

function rollDice() {
    const diceInput = document.getElementById('diceInput');
    const resultElement = document.getElementById('result');

    const notations = diceInput.value.split(',').map(item => item.trim());

    let totalResults = '';

    notations.forEach(notation => {
        const [dicePart, modifierPart] = notation.split(/(?=[-+*/])/);

        let [numDice, numSides] = (dicePart || '1d6').split('d').map(Number);
        numSides = isNaN(numSides) ? 6 : numSides;

        // Set default for numDice if not provided or if it's less than 1
        numDice = isNaN(numDice) || numDice < 1 ? 1 : numDice;

        const individualResults = [];
        let total = 0;

        for (let i = 0; i < numDice; i++) {
            const dieResult = Math.floor(Math.random() * numSides) + 1;
            individualResults.push(dieResult);
            total += dieResult;
        }

        let modifier = 0;
        if (modifierPart) {
            const operator = modifierPart.charAt(0);
            const operand = parseFloat(modifierPart.slice(1));

            switch (operator) {
                case '+':
                    modifier = operand;
                    total += modifier; // Apply the modifier directly to the total
                    break;
                case '-':
                    modifier = operand;
                    total -= modifier; // Subtract the modifier directly from the total
                    break;
                case '*':
                    modifier = operand;
                    total *= modifier; // Apply multiplication to the total
                    break;
                case '/':
                    modifier = operand;
                    total = Math.floor(total / modifier); // Round down for division
                    break;
                default:
                    break;
            }
        }

        const resultHTML = individualResults.map(dieResult => {
            const color = dieResult === numSides ? 'green' : (dieResult === 1 ? 'red' : 'white');
            return `<span style="color: ${color}">${dieResult}</span>`;
        }).join(', ');

        const modifierText = modifier !== 0 ? ` ${modifierPart}` : '';
        totalResults += `Result (${notation}): ${total} (${resultHTML})${modifierText}<br>`;
    });

    resultElement.innerHTML = totalResults;
}
