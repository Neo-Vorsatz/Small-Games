// Neo Vorsatz
// 13 November 2023

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.Random;

class Minesweeper
{
   static private final int GRID_SIZE = 10; //Change this constant to change the grid size
   static private GameWindow activeGame;
   
   static class Tile extends JButton
   //Class that represents each tile of the game
   {
      private boolean isBomb; //Each tile is either a bomb or not
      private int pos; //Each tile has a position on the grid
      
      public Tile(boolean isBomb, int pos)
      {
         super("");
         this.isBomb = isBomb;
         setActionCommand(Integer.toString(pos));
      }
      
      public boolean isBomb()
      {
         return isBomb;
      }
   }
   
   static class GameWindow extends JFrame implements ActionListener
   //Class that manages the entire functioning of the game
   {
      private boolean gameActive;
      private JPanel pnlMenu;
      private JLabel lblTop;
      private JButton btnNewGame;
      private JPanel pnlGame;
      private Tile[] tiles;
      private int safeTiles;
      
      public GameWindow() //Constructor, upon which a new game is started
      {
         //Set up layout of the window
         super("Minesweeper");
         setSize(50*GRID_SIZE, 50*GRID_SIZE+50);
         setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
         setLayout(new BorderLayout());
         getContentPane().setBackground(Color.LIGHT_GRAY);
         
         //Set up layout of the top menu
         pnlMenu = new JPanel();
         pnlMenu.setLayout(new FlowLayout());
         add(pnlMenu, BorderLayout.NORTH);
         lblTop = new JLabel("Game in Progress");
         pnlMenu.add(lblTop);
         btnNewGame = new JButton("New Game");
         btnNewGame.addActionListener(this);
         btnNewGame.setActionCommand("New Game");
         pnlMenu.add(btnNewGame);
         
         //Set up layout of the grid/game
         pnlGame = new JPanel();
         pnlGame.setLayout(new GridLayout(GRID_SIZE,GRID_SIZE));
         pnlGame.setBackground(Color.BLACK);
         add(pnlGame, BorderLayout.CENTER);
         
         //Add each tile to the game, keeping track of how many safe tiles there are
         safeTiles = GRID_SIZE*GRID_SIZE;
         tiles = new Tile[GRID_SIZE*GRID_SIZE];
         Tile tile;
         boolean isBomb;
         for (int i=0; i<(GRID_SIZE*GRID_SIZE); i++)
         {
            isBomb = (Math.random()<0.1);
            if (isBomb)
               safeTiles--;
            tile = new Tile(isBomb, i);
            tile.addActionListener(this);
            pnlGame.add(tile);
            tiles[i] = tile;
         }
         
         gameActive = true;
         setVisible(true);
      }
      
      public void mine(int index)
      //Method to "mine" tile; reveal if it's a bomb, or how many nearby bombs there are
      {
         if (tiles[index].isBomb())
         {
            tiles[index].setText("X");
            tiles[index].setEnabled(false);
            lblTop.setText("OOPS! You hit a mine!");
            gameActive = false;
            return;
         }
         safeTiles--;
         
         int bombCount = countBombs(index);
         tiles[index].setText(Integer.toString(bombCount));
         if (bombCount!=0) //If the tile has 0 mines, then we leave is Active so that autoMine() will notice it
            tiles[index].setEnabled(false);
      }
      
      public int countBombs(int index)
      {
         //Check if there are tiles to the right, top, left and bottom of this tile
         boolean rightValid = ((index%GRID_SIZE) != (GRID_SIZE-1));
         boolean topValid = (index >= GRID_SIZE);
         boolean leftValid = ((index%GRID_SIZE) != 0);
         boolean bottomValid = (index < GRID_SIZE*(GRID_SIZE-1));
         
         int bombCount = 0;
         
         //Check up to 8 adjacent squares for nearby bombs
         if (rightValid)
            if (tiles[index+1].isBomb())
               bombCount++;
         if (rightValid&&topValid)
            if (tiles[index-GRID_SIZE+1].isBomb())
               bombCount++;
         if (topValid)
            if (tiles[index-GRID_SIZE].isBomb())
               bombCount++;
         if (topValid&&leftValid)
            if (tiles[index-GRID_SIZE-1].isBomb())
               bombCount++;
         if (leftValid)
            if (tiles[index-1].isBomb())
               bombCount++;
         if (leftValid&&bottomValid)
            if (tiles[index+GRID_SIZE-1].isBomb())
               bombCount++;
         if (bottomValid)
            if (tiles[index+GRID_SIZE].isBomb())
               bombCount++;
         if (rightValid&&bottomValid)
            if (tiles[index+GRID_SIZE+1].isBomb())
               bombCount++;
         
         return bombCount;
      }
      
      public void actionPerformed(ActionEvent e)
      {
         //A new game was requested
         if (e.getActionCommand().equals("New Game"))
         {
            activeGame.setVisible(false);
            activeGame = new GameWindow();
            return;
         }
         //else a tile button must have been pressed
         
         if (!gameActive) //If the game is finished, exit the method
            return;
         
         int index = Integer.parseInt(e.getActionCommand()); //Get the index of the clicked tile
         mine(index);
         
         //Use autoMine() to automatically mine around squares with 0 adjacent bombs
         boolean allMined;
         do
            allMined = autoMine();
         while (!allMined);
         
         if (safeTiles==0) //If we've mined all safe tiles, then we win the game
         {
            lblTop.setText("CONGRATULATIONS! You avoided every mine!");
            gameActive = false;
         }
      }
      
      public boolean autoMine()
      {
         boolean allMined = true;
         for (int index=0; index<(GRID_SIZE*GRID_SIZE); index++) //For every tile in the game
         {
            if (tiles[index].getText().equals("0") && tiles[index].isEnabled()) //Check if that tile is a 0 and hasn't already been dealt with
            {
               tiles[index].setEnabled(false);
               allMined = false; //Setting this to false notes that we haven't mined around every 0
               
               //Check if there are tiles to the right, top, left and bottom of this tile
               boolean rightValid = ((index%GRID_SIZE) != (GRID_SIZE-1));
               boolean topValid = (index >= GRID_SIZE);
               boolean leftValid = ((index%GRID_SIZE) != 0);
               boolean bottomValid = (index < GRID_SIZE*(GRID_SIZE-1));
               
               //Mine up to 8 adjacent tiles
               if (rightValid)
                  if (tiles[index+1].getText().equals(""))
                     mine(index+1);
               if (rightValid&&topValid)
                  if (tiles[index-GRID_SIZE+1].getText().equals(""))
                     mine(index-GRID_SIZE+1);
               if (topValid)
                  if (tiles[index-GRID_SIZE].getText().equals(""))
                     mine(index-GRID_SIZE);
               if (topValid&&leftValid)
                  if (tiles[index-GRID_SIZE-1].getText().equals(""))
                     mine(index-GRID_SIZE-1);
               if (leftValid)
                  if (tiles[index-1].getText().equals(""))
                     mine(index-1);
               if (leftValid&&bottomValid)
                  if (tiles[index+GRID_SIZE-1].getText().equals(""))
                     mine(index+GRID_SIZE-1);
               if (bottomValid)
                  if (tiles[index+GRID_SIZE].getText().equals(""))
                     mine(index+GRID_SIZE);
               if (rightValid&&bottomValid)
                  if (tiles[index+GRID_SIZE+1].getText().equals(""))
                     mine(index+GRID_SIZE+1);
            }
         }
         
         return allMined;
      }
   }
   
   public static void main(String[] args)
   {
      activeGame = new GameWindow(); //Start the first game
   }
}