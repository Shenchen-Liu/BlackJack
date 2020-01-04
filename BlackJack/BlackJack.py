import  random,time
import pygame
#定义界面上各个按钮的大小和坐标
cardWidth = 105
startBtn_Size = (262,119)
startBtn_XY = (333,350)
operateBtn_Size = (134,55)
dealBtn_XY = (684,70)
hitBtn_XY = (684,213)
standBtn_XY = (684,356)
dealCardsPos = (30, 81)
playerCardsPos = (486, 278)
#判断鼠标位置是否在某个区域内，即判定点没点击按钮
def if_inRect(pos,XY,size):
    if pos[0] in range(XY[0], XY[0] + size[0] + 1) \
            and pos[1] in range(XY[1], XY[1] + size[1] + 1):
        return True
    else:
        return False
'''
    定义扑克牌类，每个对象代表一张牌
'''
class Card():
    def __init__(self,card_type,card_text,card_value):
        '''
        初始化方法
        :param card_type: 牌面类型 ♠♥♦♣
        :param card_text: 牌面内容 A J Q K
        :param card_value: 牌面点数
        '''
        self.card_type =  card_type
        self.card_text = card_text
        self.card_value = card_value
        self.car_imgName = card_type + card_text
'''
    定义荷官类，一个对象代表一局荷官实现取牌和发牌的作用
'''
class Dealer:
    def __init__(self):
        """初始化方法"""
        # 定义列表，用来保存一整副扑克牌（52张）
        self.cards = []
        # 定义所有牌的类型。
        all_card_type = "♥♠♣♦"
        # 定义所有牌面显示的文本
        all_card_text = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        # 定义牌面文本对应的真实点数
        all_card_value = [1, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        # 对牌面类型与牌面文本进行嵌套循环。
        for card_type in all_card_type:
            for index, card_text in enumerate(all_card_text):
                # 创建Card类型的对象。（一张扑克牌）
                card = Card(card_type, card_text, all_card_value[index])
                # 将创建好的card对象加入到整副扑克牌当中。
                self.cards.append(card)
        # 洗牌操作
        random.shuffle(self.cards)

    def send_card(self, role, num=1):
        """
        给电脑或者玩家发牌。
        -----
        role : Role
            电脑或玩家对象。
        num ： int
            发牌的张数。默认为1。
        """
        for i in range(num):
            card = self.cards.pop()
            role.cards_in_hand.append(card)
        role.calc_point()
'''
    定义角色类，分别生成玩家和电脑对象
'''
class Role():
    def __init__(self):
        '''
        初始化实例属性
        cards_in_hand:手中的扑克牌
        point:牌面总点数
        '''
        self.points = 0
        self.cards_in_hand = []

    def calc_point(self):
        '''
        计算牌面点数
        '''
        self.points = 0
        for card in self.cards_in_hand:
            self.points += card.card_value
        for card in self.cards_in_hand:
        # 判断是否有A，如果有A再判断是否小于21，如果是的话A当做11，否的话当做1
            if card.card_text == 'A' and self.points + 10 < 21:
                self.points += 10
    def burst(self):
        """
        判断是否爆牌，是返回True，否则返回False。
        Returns
        -----
        b : bool
            是否爆牌，爆牌返回True，否则返回False。
        """
        # 判断是否爆牌，只需要判断最小值是否大于21点即可。
        self.calc_point()
        return self.points > 21


    def get_card(self, *cards):
        '''
        玩家取荷官发的牌，并更新计数器
        param： *cards 一个或多个list类型表示的牌
        '''
        for card in cards:
            self.cards_in_hand.append(card)
        self.calc_points() # 计算分数
''' 
    定一个游戏类，创建一个对象即开始一个游戏进程
'''
class BlackJack():
    def __init__(self):
        self.gameOver = False  #判断是否退出游戏
        self.startGame = False  #判断是否开始游戏
        #游戏开始，分别创建一个荷官、电脑和玩家对象
        self.dealer = Dealer()
        self.computer = Role()
        self.player = Role()
        self.hit = False    #判断是否要牌阶段
        self.stand = False  #判断是否停牌阶段
        self.currentGame = False #判断本轮游戏是否开始
        #初始化pygame
        pygame.init()
        self.window = pygame.display.set_mode((840, 500))
        self.font = pygame.font.Font('fonts/思源黑体.otf', 15)
    #初始化每一轮游戏
    def game_init(self):
        #卡牌清空
        self.computer.cards_in_hand = []
        self.player.cards_in_hand = []
        self.hit = False
        self.stand = False
    #初始化开始界面
    def startUiInit(self):
        pygame.display.set_caption('BlackJack')

        startBack = pygame.image.load('images/startBack.png')
        startBtn = pygame.image.load('images/startBtn.png')
        self.window.fill((0,0,0))
        self.window.blit(startBack, (0, 0))
        self.window.blit(startBtn, (333, 350))
    #初始化游戏界面
    def gameUiInit(self):
        table = pygame.image.load('images/table.png')
        dealBtn = pygame.image.load('images/dealBtn.png')
        hitBtn = pygame.image.load('images/hitBtn.png')
        standBtn = pygame.image.load('images/standBtn.png')
        self.window.blit(table,(0,0))
        self.window.blit(dealBtn,dealBtn_XY)
        self.window.blit(hitBtn,hitBtn_XY)
        self.window.blit(standBtn,standBtn_XY)
    #获取游戏事件，具体表现是鼠标点击那些地方
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#点击窗口关闭，游戏退出结束
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:#获取鼠标点击事件
                mousePos = pygame.mouse.get_pos()#获取鼠标位置
                #如果游戏还没开始，则显示的是开始界面，需要点击"开始游戏"进入游戏界面
                if not self.startGame:
                    #点击开始游戏按钮
                    if if_inRect(mousePos,startBtn_XY,startBtn_Size):
                        self.startGame = True
                else:
                    #点击发牌按钮
                    if if_inRect(mousePos,dealBtn_XY,operateBtn_Size):
                        self.currentGame = True
                        self.game_init()
                        #分别给电脑，玩家发两张牌
                        self.dealer.send_card(self.computer,2)
                        self.dealer.send_card(self.player, 2)
                    if self.currentGame:
                        #点击要牌按钮
                        if if_inRect(mousePos,hitBtn_XY,operateBtn_Size):
                            self.hit = True
                            self.dealer.send_card(self.player,1)
                        #点击停牌按钮
                        if if_inRect(mousePos,standBtn_XY,operateBtn_Size):
                            self.hit = False
                            self.stand = True
        return False
    #显示桌上的牌面
    def show_cards(self):
        for i in range(len(self.computer.cards_in_hand)):
            if self.currentGame :#如果这一轮还没结束，则电脑的第一张牌盖住
                if i == 0:
                    cardImg = pygame.image.load('images/back.jpg')
                else:
                    cardFile = self.computer.cards_in_hand[i].card_type + self.computer.cards_in_hand[i].card_text
                    cardImg = pygame.image.load('images/' + cardFile + '.jpg')
            else:
                cardFile = self.computer.cards_in_hand[i].card_type + self.computer.cards_in_hand[i].card_text
                cardImg = pygame.image.load('images/' + cardFile + '.jpg')
            self.window.blit(cardImg, (dealCardsPos[0] + cardWidth * i, dealCardsPos[1]))
        for i in range(len(self.player.cards_in_hand)):
            cardFile = self.player.cards_in_hand[i].card_type + self.player.cards_in_hand[i].card_text
            cardImg = pygame.image.load('images/' + cardFile + '.jpg')
            self.window.blit(cardImg, (playerCardsPos[0] - cardWidth * i, playerCardsPos[1]))

    #庄家要牌并判定本轮游戏结果
    def computer_hitCard(self):
        # 如果没有爆牌，则判断庄家的牌面值是否达到17点，如果达到17点，则庄家必须停牌，否则，庄家必须继续要牌。
        self.computer.calc_point()
        if self.computer.points < 17:
            time.sleep(1)
            self.dealer.send_card(self.computer, 1)
        #庄家要牌结束，判断谁赢了
        else:
            self.is_win()
    #检查是否爆牌
    def check(self):
        if self.player.burst():
            text = self.font.render('玩家爆牌！庄家获胜！游戏结束！！！！',True,(255,255,255))
            self.window.blit(text,(840/2,480))
            self.currentGame = False
        if self.computer.burst():
            text = self.font.render('庄家爆牌！玩家获胜！游戏结束！！！！',True,(255,255,255))
            self.window.blit(text,(840/2,480))
            self.currentGame = False
    #判断谁赢了
    def is_win(self):
        if not self.computer.burst() and not self.player.burst():
            self.computer.calc_point()
            self.player.calc_point()
            player_points = self.player.points
            computer_points = self.computer.points
            result = ''
            if player_points > computer_points:
                result = f"玩家点数为{player_points}, 电脑点数为{computer_points}, 玩家赢了！"
            elif player_points == computer_points:
                result = f"玩家点数为{player_points}, 电脑点数为{computer_points}, 平局！"
            else:
                result = f"玩家点数为{player_points}, 电脑点数为{computer_points}, 电脑赢了！"
            text = self.font.render(result,True,(255,255,255))
            self.window.blit(text, (840/2, 480))
            self.currentGame = False
if __name__ == '__main__':
    game = BlackJack()#创建一个游戏对象
    gameOver = False
    while not gameOver:#开始游戏进程
        game.startUiInit()#开始界面
        gameOver = game.process_events()#获取事件，是否点击了"开始游戏"
        if game.startGame:
            game.gameUiInit()#游戏棋盘界面
            game.show_cards()#展示扑克牌
            if game.hit:#一边要牌一边检查是否爆牌
                game.check()
            if game.stand:#要牌结束，停牌，庄家开始边要牌边检查，并判断结果
                game.check()
                game.computer_hitCard()
        #实时游戏更新界面
        pygame.display.update()
    pygame.quit()

