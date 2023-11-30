namespace ConcertBoxxd.Data
{
    public class Song
    {
        public int ID { get; set; }
        public string Name { get; set; }

        public Song()
        { }
        public Song(int id, string name)
        {
            ID = id;
            Name = name;
        }


        //might need to add a ToString() override
    }
}
