document.addEventListener('DOMContentLoaded', () => {
            const basket = document.getElementById('basket');
            const popup = document.getElementById('popup');
            const overlay = document.getElementById('overlay');
            const basketContent = document.getElementById('basketContent');
            const orderButtons = document.querySelectorAll('.order-button');

            let dishesInBasket = {};
            function addDishToBasket(dishName, price) {
                if (dishesInBasket[dishName]) {
                    dishesInBasket[dishName].quantity += 1; // Увеличиваем количество
                } else {
                    dishesInBasket[dishName] = { quantity: 1, price }; // Добавляем новое блюдо
                }
                renderBasketContents();
            }

            function renderBasketContents() {
                basketContent.innerHTML = ''; // Очистка текущего содержимого
                let total = 0; // Сумма заказываемых блюд
                let emptyMessage = document.createElement('div'); // Сообщение о пустой корзине

                // Добавление каждого блюда в список
                for (const dish in dishesInBasket) {
                    const { quantity, price } = dishesInBasket[dish];

                    const item = document.createElement('div');
                    item.classList.add('basket-item');

                    const itemDetails = document.createElement('div');
                    itemDetails.classList.add('item-details');
                    itemDetails.textContent = `${dish} - ${price} ₽`;

                    const quantityContainer = document.createElement('div');
                    quantityContainer.style.display = 'flex';
                    quantityContainer.style.alignItems = 'center';
                    quantityContainer.style.justifyContent = 'flex-end';

                    const decreaseButton = document.createElement('button');
                    decreaseButton.textContent = '-';
                    const quantityLabel = document.createElement('span');
                    quantityLabel.textContent = quantity;

                    // Отступ между кнопками и количеством
                    quantityLabel.style.margin = '0 10px';
                    decreaseButton.style.marginRight = '1px'; // Отступ для кнопки -

                    const increaseButton = document.createElement('button');
                    increaseButton.textContent = '+';
                    increaseButton.style.marginLeft = '1px'; // Отступ для кнопки +

                    decreaseButton.addEventListener('click', () => {
                        if (quantity > 1) {
                            dishesInBasket[dish].quantity -= 1; // Уменьшаем количество
                        } else {
                            delete dishesInBasket[dish]; // Удаляем блюдо, если количество 1
                        }
                        renderBasketContents(); // Обновляем корзину
                    });

                    increaseButton.addEventListener('click', () => {
                        addDishToBasket(dish, price); // Увеличение количества
                    });

                    quantityContainer.appendChild(decreaseButton);
                    quantityContainer.appendChild(quantityLabel);
                    quantityContainer.appendChild(increaseButton);
                    item.appendChild(itemDetails);
                    item.appendChild(quantityContainer);
                    basketContent.appendChild(item);

                    // Вычисляем общую сумму
                    total += price * quantity; 
                }

                // Проверка на пустоту корзины
                if (Object.keys(dishesInBasket).length === 0) {
                    emptyMessage.textContent = "Корзина пустая";
                    emptyMessage.style.textAlign = "center"; // Центрируем текст
                    basketContent.appendChild(emptyMessage);
                }

                // Создаем элемент для отображения итоговой суммы
                const totalElement = document.createElement('div');
                 totalElement.textContent = `Итого: ${total} ₽`;
                totalElement.style.textAlign = 'center'; // Центрируем текст
                totalElement.style.marginTop = '10px'; // Отступ сверху

                basketContent.appendChild(totalElement);
            }

            // Обработчики событий для каждой кнопки "Заказать"
            orderButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const dishName = e.target.parentElement.children[0].innerText; // Получаем текст блюда
                    const price = e.target.parentElement.dataset.price; // Получаем цену блюда
                    addDishToBasket(dishName, price); // Добавляем его в корзину
                });
            });

            // Открытие/закрытие всплывающего окна корзины
            basket.addEventListener('click', (e) => {
                e.preventDefault();
                popup.classList.toggle('active');
                overlay.classList.toggle('active');
            });

            // Закрытие всплывающего окна при клике на подложку
            overlay.addEventListener('click', () => {
                popup.classList.remove('active');
                overlay.classList.remove('active');
            });

            // Оформление заказа (добавьте нужную вам логику)
            document.getElementById('checkout').addEventListener('click', () => {
                alert('Ваш заказ оформлен!');
            });
        });